"""Input validation utilities for xlschema.

This module provides secure validation functions for user inputs
to prevent security vulnerabilities and ensure data integrity.
"""
import os
import re
import logging
from pathlib import Path
from typing import Union, List
from urllib.parse import urlparse

from sqlalchemy.engine.url import make_url
from sqlalchemy.exc import ArgumentError

# Define ValidationError locally to avoid circular imports
class ValidationError(Exception):
    """Raised when input validation fails."""
    pass


logger = logging.getLogger(__name__)


def validate_path(path: Union[str, Path], must_exist: bool = False,
                  allowed_extensions: List[str] = None) -> Path:
    """Validate file or directory path.

    :param path: path to validate
    :param must_exist: if True, path must exist
    :param allowed_extensions: list of allowed file extensions (e.g. ['.yml', '.xlsx'])
    :raises ValidationError: if path is invalid or unsafe
    :returns: validated Path object
    """
    if not path:
        raise ValidationError("Path cannot be empty")

    # Convert to Path object
    try:
        path_obj = Path(path).resolve()
    except (OSError, ValueError) as e:
        raise ValidationError(f"Invalid path format: {e}")

    # Check for path traversal attempts
    path_str = str(path_obj)
    if '..' in path_str or path_str.startswith('/'):
        # Allow absolute paths but log for security monitoring
        logger.warning("Absolute path provided: %s", path_str)

    # Validate against null bytes and control characters
    if '\x00' in str(path) or any(ord(c) < 32 for c in str(path) if c not in '\t\n\r'):
        raise ValidationError("Path contains invalid characters")

    # Check if path must exist
    if must_exist and not path_obj.exists():
        raise ValidationError(f"Path does not exist: {path_obj}")

    # Check file extension if specified
    if allowed_extensions and path_obj.is_file():
        if not any(str(path_obj).lower().endswith(ext.lower()) for ext in allowed_extensions):
            raise ValidationError(f"File extension not allowed. Allowed: {allowed_extensions}")

    return path_obj


def validate_uri(uri: str) -> str:
    """Validate database or file URI.

    :param uri: URI to validate
    :raises ValidationError: if URI is invalid or unsafe
    :returns: validated URI string
    """
    if not uri or not isinstance(uri, str):
        raise ValidationError("URI must be a non-empty string")

    # Check for null bytes and control characters
    if '\x00' in uri or any(ord(c) < 32 for c in uri if c not in '\t\n\r'):
        raise ValidationError("URI contains invalid characters")

    # If it looks like a file path, validate as path
    if not ('://' in uri or uri.startswith('sqlite:///')):
        try:
            # For file URIs, be more permissive but still validate for security
            validate_path(uri, must_exist=False)  # Don't require existence for backward compatibility
            return uri
        except ValidationError as e:
            # If basic path validation fails, it's a security issue
            raise ValidationError(f"Invalid file URI: {e}")

    # Validate as database URI
    try:
        parsed_url = make_url(uri)

        # Check for suspicious components
        if parsed_url.password and len(parsed_url.password) > 256:
            logger.warning("Unusually long password in URI")

        if parsed_url.database and ('..' in parsed_url.database or '/' in parsed_url.database):
            logger.warning("Suspicious database name in URI: %s", parsed_url.database)

        return uri

    except ArgumentError as e:
        raise ValidationError(f"Invalid database URI: {e}")


def validate_sql_query(query: str, max_length: int = 10000) -> str:
    """Validate SQL query for safety.

    :param query: SQL query string to validate
    :param max_length: maximum allowed query length
    :raises ValidationError: if query is invalid or potentially unsafe
    :returns: validated query string
    """
    if not query or not isinstance(query, str):
        raise ValidationError("SQL query must be a non-empty string")

    # Check length
    if len(query) > max_length:
        raise ValidationError(f"SQL query too long (max {max_length} chars)")

    # Check for null bytes and control characters
    if '\x00' in query:
        raise ValidationError("SQL query contains null bytes")

    # Remove comments and whitespace for analysis
    cleaned_query = re.sub(r'--.*$|/\*.*?\*/', '', query, flags=re.MULTILINE | re.DOTALL)
    cleaned_query = cleaned_query.strip().lower()

    # Check for potentially dangerous SQL patterns
    dangerous_patterns = [
        r'\bexec\s*\(',         # exec() calls
        r'\bexit\s*\(',         # exit() calls
        r'\bsystem\s*\(',       # system() calls
        r'\b\$\$.*\$\$',        # PostgreSQL dollar quoting
        r'\binto\s+outfile\b',  # MySQL file operations
        r'\bload_file\s*\(',    # MySQL file reading
        r'\bxp_cmdshell\b',     # SQL Server command execution
        r'\bsp_execute\b',      # SQL Server stored proc execution
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, cleaned_query, re.IGNORECASE):
            raise ValidationError(f"SQL query contains potentially dangerous pattern: {pattern}")

    # Warn about DDL operations (they might be intentional but worth logging)
    ddl_patterns = [r'\bdrop\s+\w+\b', r'\bcreate\s+\w+\b', r'\balter\s+\w+\b', r'\btruncate\s+\w+\b']
    for pattern in ddl_patterns:
        if re.search(pattern, cleaned_query, re.IGNORECASE):
            logger.warning("SQL query contains DDL operation: %s", query[:100])

    return query


def validate_table_name(table_name: str) -> str:
    """Validate database table name.

    :param table_name: table name to validate
    :raises ValidationError: if table name is invalid
    :returns: validated table name
    """
    if not table_name or not isinstance(table_name, str):
        raise ValidationError("Table name must be a non-empty string")

    # Check length (most databases have limits around 63-128 chars)
    if len(table_name) > 63:
        raise ValidationError("Table name too long (max 63 chars)")

    # Check for valid identifier pattern (letters, numbers, underscores)
    if not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', table_name):
        raise ValidationError("Table name contains invalid characters (use letters, numbers, underscores only)")

    # Check for SQL reserved words (basic check)
    reserved_words = {
        'select', 'insert', 'update', 'delete', 'drop', 'create', 'alter',
        'table', 'database', 'index', 'view', 'trigger', 'procedure', 'function',
        'user', 'role', 'grant', 'revoke', 'commit', 'rollback', 'union', 'order'
    }

    if table_name.lower() in reserved_words:
        raise ValidationError(f"Table name '{table_name}' is a reserved SQL keyword")

    return table_name


def validate_format_string(format_str: str, allowed_formats: List[str] = None) -> str:
    """Validate output format string.

    :param format_str: format string like 'py/djmodels'
    :param allowed_formats: list of allowed format strings
    :raises ValidationError: if format is invalid
    :returns: validated format string
    """
    if not format_str or not isinstance(format_str, str):
        raise ValidationError("Format string must be non-empty")

    # Check for basic format pattern
    if not re.match(r'^[a-zA-Z0-9_]+/[a-zA-Z0-9_]+$', format_str):
        raise ValidationError("Format must be in 'category/method' pattern")

    # Check against allowed formats if provided
    if allowed_formats and format_str not in allowed_formats:
        raise ValidationError(f"Format '{format_str}' not in allowed formats: {allowed_formats}")

    return format_str