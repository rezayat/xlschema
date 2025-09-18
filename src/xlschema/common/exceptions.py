"""Custom exceptions for xlschema.

This module provides specific exception classes for better error handling
and more informative error messages throughout the application.
"""


class XLSchemaError(Exception):
    """Base exception for all xlschema-related errors."""
    pass


class ValidationError(XLSchemaError):
    """Raised when input validation fails."""
    pass


class URIError(XLSchemaError):
    """Raised when URI parsing or validation fails."""
    pass


class ReaderError(XLSchemaError):
    """Raised when schema reading fails."""
    pass


class WriterError(XLSchemaError):
    """Raised when code generation/writing fails."""
    pass


class TemplateError(XLSchemaError):
    """Raised when template rendering fails."""
    pass


class ConfigurationError(XLSchemaError):
    """Raised when configuration is invalid or missing."""
    pass


class PluginError(XLSchemaError):
    """Raised when plugin execution fails."""
    pass


class SchemaParsingError(ReaderError):
    """Raised when schema parsing from Excel/YAML fails."""

    def __init__(self, message: str, file_path: str = None, sheet_name: str = None):
        """Initialize with context information.

        :param message: error description
        :param file_path: path to file being parsed
        :param sheet_name: name of sheet being parsed (for Excel files)
        """
        self.file_path = file_path
        self.sheet_name = sheet_name

        full_message = message
        if file_path:
            full_message += f" (file: {file_path}"
            if sheet_name:
                full_message += f", sheet: {sheet_name}"
            full_message += ")"

        super().__init__(full_message)


class SQLExecutionError(ReaderError):
    """Raised when SQL execution fails."""

    def __init__(self, message: str, query: str = None, database: str = None):
        """Initialize with context information.

        :param message: error description
        :param query: SQL query that failed
        :param database: database connection string
        """
        self.query = query
        self.database = database

        full_message = message
        if query:
            # Truncate long queries for error messages
            query_preview = query[:100] + "..." if len(query) > 100 else query
            full_message += f" (query: {query_preview}"
            if database:
                full_message += f", database: {database}"
            full_message += ")"

        super().__init__(full_message)


class TemplateRenderingError(TemplateError):
    """Raised when template rendering fails."""

    def __init__(self, message: str, template_name: str = None, context_keys: list = None):
        """Initialize with context information.

        :param message: error description
        :param template_name: name of template being rendered
        :param context_keys: keys available in template context
        """
        self.template_name = template_name
        self.context_keys = context_keys

        full_message = message
        if template_name:
            full_message += f" (template: {template_name}"
            if context_keys:
                full_message += f", context keys: {list(context_keys)}"
            full_message += ")"

        super().__init__(full_message)