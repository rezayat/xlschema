# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

XLSchema is a Python 3 tool and library for generating boilerplate code for relational database models from YAML files, MS Excel templates, or directly from database connections. It supports round-trip conversion to multiple target formats including SQL, Django models, SQLAlchemy, Haskell, and more.

## Development Environment

This project uses [rye](https://rye.astral.sh/guide/) as the development tool and package manager.

### Setup Commands

```bash
# Initial setup
rye sync
source .venv/bin/activate

# Install development dependencies
rye sync --dev
```

## Common Commands

### Testing

```bash
# Run fast tests (skip slow ones)
pytest -k-slow

# Run all tests
pytest

# Run tests with coverage report
pytest --cov-report html:docs/coverage --cov=xlschema

# Run tests with timing (show 20 slowest)
pytest --durations=20

# Run tests with HTML report
pytest --html=docs/test-report.html --self-contained-html
```

### Quality Checks

```bash
# Run all quality checks
make check

# Individual checks
python3 -m pylint src/xlschema
```

### Documentation

```bash
# Build HTML documentation
make html

# Build UML diagrams
make uml

# Build PDF documentation
make pdf
```

### Code Style

```bash
# Format imports
make isort
```

### Cleaning

```bash
# Clean all artifacts
make clean

# Clean specific artifacts
make clean-pyc     # Python cache files
make clean-output  # Generated output files
make clean-tests   # Test artifacts
make clean-build   # Build artifacts
```

## Core Architecture

The project follows a plugin-based architecture with three main component types:

### 1. Readers (`src/xlschema/readers/`)
Convert input sources to internal Schema representation:
- **YamlToModel**: Reads YAML specification files
- **ExcelToModel**: Reads Excel (.xlsx) files with schema definitions
- **DBToModel**: Reads database schema via connection URIs
- **SqlToModel**: Executes SQL queries against databases

### 2. Core Models (`src/xlschema/models.py`)
- **Schema**: Primary container for models and enums
- **Model**: Represents database tables with fields and relationships
- **Enum**: Represents enumeration types
- **Namespace**: Provides code generation context for models

### 3. Writers (`src/xlschema/writers/`)
Convert internal Schema to target formats:
- **SQL**: PostgreSQL, SQLite, with enum support
- **Python**: Django models, SQLAlchemy, pandas, factories
- **Other**: Java/Hibernate, Haskell, R, CSV, YAML, documentation

### Plugin System (`src/xlschema/plugins/`)
- **CorePlugin**: Main `from_uri` command functionality
- **DisplayPlugin**: Shows available writers
- **SplitterPlugin**: Splits Excel sheets

## Key Usage Patterns

### CLI Usage
```bash
# Generate all formats from YAML
python3 -m xlschema from_uri tests/data/yml/node.yml

# Generate specific format
python3 -m xlschema from_uri --format=sql/postgres tests/data/yml/node.yml

# From database
python3 -m xlschema from_uri sqlite:///data/db/test.sqlite --format=py/djmodels

# Multiple specific tables
python3 -m xlschema from_uri <db_uri> --table person vehicle
```

### Library Usage
```python
from xlschema import XLSchema

# Create instance
xlschema = XLSchema('path/to/schema.yml', options)

# Write to specific format
xlschema.write('py/djmodels')

# Write all formats
xlschema.write()
```

## Configuration

- **Config Class**: `src/xlschema/config.py` - Central configuration
- **Writer Registration**: Writers self-register using `@register` decorator
- **Template System**: Uses Mako templates in `src/xlschema/resources/templates/`
- **Local Directory**: `.xlschema/` for local output and templates

## Field Types and Metadata

Models support rich field metadata:
- **Types**: str, int, date, time, bool, dec, float, etc.
- **Indexes**: pk (primary key), fk (foreign key), sk (semantic key), pfk (primary foreign key)
- **Constraints**: enum, required, length, default values
- **Categories**: For grouping related fields

## Testing Data

Test data located in `tests/data/`:
- `yml/`: YAML schema examples
- `xlsx/`: Excel template examples
- `db/`: SQLite test databases
- `output/`: Generated output files

## Important Notes

- All writers must inherit from `SchemaWriter` and register with `@register`
- Field classes are specialized per target language (Python, Java, SQL, etc.)
- Schema validation ensures enum fields have corresponding enum definitions
- Models support hierarchical relationships and many-to-many tables
- Template-based code generation allows easy customization

## Code Review Summary

This comprehensive code review was conducted to assess the overall quality, structure, and maintainability of the xlschema codebase (~6,470 lines of Python code).

### Strengths

**Architecture & Design**
- Well-structured plugin-based architecture with clear separation of concerns
- Clean abstraction layers: Readers → Models → Writers pattern
- Comprehensive template system using Mako for code generation
- Good use of inheritance hierarchies (SchemaWriter → TemplateWriter → MultiTemplateWriter)
- Strong type validation and enum constraint checking

**Code Organization**
- Logical module structure with appropriate separation
- Consistent naming conventions throughout codebase
- Good use of abstract base classes to enforce contracts
- Clean field metadata system with 55+ supported formats

**Testing Coverage**
- Extensive test suite with 53+ test files covering unit and integration tests
- Parametrized fixtures for testing multiple input formats (YAML/Excel)
- Good separation of test data and expected outputs
- Comprehensive format testing across all supported writers

**Configuration & Tooling**
- Well-configured development tools (pylint, pytest, coverage, flake8)
- Proper CI/CD setup with quality gates
- Good documentation generation with Sphinx
- Makefile with comprehensive automation

### Areas for Improvement

**Security Concerns** ⚠️
- **High Priority**: Direct use of `os.system()` in mixins.py:12 and depends.py:142 creates shell injection vulnerabilities
- Database connections use string formatting which could be susceptible to SQL injection
- No input sanitization on user-provided paths or URIs
- Template rendering accepts arbitrary user input without validation

**Error Handling**
- Inconsistent error handling patterns across modules
- Some bare `except:` clauses (readers/db/__init__.py:115)
- Critical errors use `sys.exit(1)` instead of proper exception handling
- Limited error context in exception messages

**Code Quality Issues**
- Mixed logging levels (debug/info/warning) without clear guidelines
- Some long functions that could be refactored (xl_to_model.py)
- Hardcoded constants scattered throughout code
- Limited docstring coverage in some modules

**Dependencies & Compatibility**
- Pinned SQLAlchemy to specific version (1.4.54) may cause compatibility issues
- Limited Python version support (>=3.12.3 changed to >=3.8)
- Heavy dependency on openpyxl and Mako templates

### Recommendations

**Immediate Actions**
1. **Replace `os.system()` calls** with `subprocess.run()` for security
2. **Add input validation** for all user-provided data (paths, URIs, SQL)
3. **Implement proper exception handling** instead of `sys.exit()`
4. **Add parameter validation** in template rendering

**Medium-term Improvements**
1. Add comprehensive type hints throughout codebase
2. Implement structured logging with consistent levels
3. Add integration tests for security-sensitive operations
4. Consider dependency injection for better testability
5. Add automated security scanning to CI/CD pipeline

**Code Quality Enhancements**
1. Increase docstring coverage to 100%
2. Break down large functions into smaller, focused methods
3. Centralize configuration and eliminate hardcoded constants
4. Add performance benchmarks for large file processing

### Migration Notes

- Recent migration from rye to uv package manager
- Consider updating SQLAlchemy to 2.x for better async support
- Template system is mature but may benefit from Jinja2 migration for broader ecosystem support

### Overall Assessment

**Rating: B+ (Good with Security Concerns)**

The xlschema project demonstrates solid software engineering practices with a clean, extensible architecture. The plugin system and template-based code generation are particularly well-designed. However, **immediate attention is required for security vulnerabilities** around shell command execution and input validation. Once these critical issues are addressed, this is a well-maintained, production-ready codebase with good test coverage and development practices.

