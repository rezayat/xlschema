# XLSchema: Modern Relational Model Code Generator

[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://python.org)
[![SQLAlchemy](https://img.shields.io/badge/sqlalchemy-2.0.43-green.svg)](https://sqlalchemy.org)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

**XLSchema** is a powerful Python 3 framework for generating boilerplate code for relational database models from multiple input sources. Convert YAML specifications, Excel templates, or existing database schemas into 25+ target formats including SQL, Python frameworks (Django, SQLAlchemy), Haskell, Java Hibernate, and more.

---

## Table of Contents

- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage Examples](#usage-examples)
  - [From YAML/Excel Files](#from-yamlexcel-files)
  - [From Database Connections](#from-database-connections)
  - [API Usage](#api-usage)
- [Command Line Interface](#command-line-interface)
- [Supported Formats](#supported-formats)
- [Configuration](#configuration)
- [Architecture](#architecture)
- [Security Features](#security-features)
- [Recent Updates](#recent-updates)
- [Contributing](#contributing)
- [Documentation](#documentation)
- [License](#license)

---

## Features

- **Multi-Source Input**: YAML files, Excel spreadsheets, or direct database connections
- **25+ Output Formats**: SQL dialects, Python frameworks, documentation, and more
- **Round-Trip Conversion**: Bidirectional conversion between formats
- **Enterprise Security**: Input validation, SQL injection prevention, secure command execution
- **Modern Stack**: SQLAlchemy 2.0, Python 3.12+, secure subprocess handling
- **Plugin Architecture**: Extensible framework for custom readers and writers
- **Rich Data Types**: Support for enums, relationships, constraints, and metadata
- **Template-Based**: Customizable Mako templates for code generation

---

## Quick Start

### Basic Example

1. **Create a schema** (`schema.yml`):

```yaml
enums:
  - name: status
    data:
      - [created,  Created]
      - [open,     Open]
      - [finished, Finished]
      - [closed,   Closed]

models:
  - name: node
    fields:
      - name: id
        type: int
        index: pk

      - name: parent_id
        type: int
        index: fk

      - name: name
        type: str
        length: 50
        required: true

      - name: status
        type: str
        length: 10
        required: true
        constraint: enum

    data:
      - [1, null, A, created]
      - [2, 1,    B, open]
      - [3, 1,    C, finished]
```

2. **Generate SQL**:

```bash
python -m xlschema from_uri --format=sql/postgres schema.yml
```

**Output** (`schema_postgres.sql`):
```sql
DROP TYPE IF EXISTS status CASCADE;
CREATE TYPE status AS ENUM (
    'created',
    'open',
    'finished',
    'closed'
);

DROP TABLE IF EXISTS node CASCADE;
CREATE TABLE node (
    id INTEGER PRIMARY KEY,
    parent_id INTEGER REFERENCES node (id),
    name VARCHAR(50) NOT NULL,
    status status NOT NULL
);
```

3. **Generate Django Models**:

```bash
python -m xlschema from_uri --format=py/djmodels schema.yml
```

**Output** (`schema_djmodels.py`):
```python
from django.db import models

STATUS = [
    ("created", "Created"),
    ("open", "Open"),
    ("finished", "Finished"),
    ("closed", "Closed"),
]

class Node(models.Model):
    id = models.IntegerField(primary_key=True)
    parent = models.ForeignKey("self", null=True, blank=True,
                              related_name="children", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    status = models.CharField(max_length=10, choices=STATUS)

    class Meta:
        db_table = "node"
        verbose_name_plural = "nodes"
```

---

## Installation

### Prerequisites

- **Python 3.12+**
- **[uv](https://github.com/astral-sh/uv)** (recommended) or pip

### From Source

```bash
git clone https://github.com/rezayat/xlschema.git
cd xlschema
uv sync
source .venv/bin/activate
```

### Development Setup

```bash
# Install with development dependencies
uv sync --dev

# Run tests
uv run pytest

# Run quality checks
uv run make check

# Generate documentation
uv run make html
```

---

## Usage Examples

### From YAML/Excel Files

```bash
# Generate all formats from YAML
python -m xlschema from_uri schema.yml

# Generate specific format
python -m xlschema from_uri --format=py/sqlalchemy schema.xlsx

# Generate multiple formats
python -m xlschema from_uri --format=sql/postgres py/django schema.yml

# Models only (no data)
python -m xlschema from_uri --models-only --format=sql/sqlite schema.yml
```

### From Database Connections

```bash
# Export entire database
python -m xlschema from_uri postgresql://user:pass@host/db

# Export specific tables
python -m xlschema from_uri sqlite:///app.db --table users orders

# Export SQL query results
python -m xlschema from_uri sqlite:///app.db --sql "SELECT * FROM active_users"

# Export to specific format
python -m xlschema from_uri mysql://user:pass@host/db --format=py/djmodels
```

### API Usage

```python
from xlschema import XLSchema

# From file
app = XLSchema('schema.yml', output='./generated')
app.write('py/sqlalchemy')

# From database
app = XLSchema('postgresql://user:pass@host/db', models_only=True)
app.write(['sql/postgres', 'py/django'])

# All available formats
app.write()  # Generates all supported formats
```

---

## Command Line Interface

### Main Commands

```bash
# View available plugins
python -m xlschema --help

# Core code generation
python -m xlschema from_uri [OPTIONS] URI

# Display available formats
python -m xlschema display

# Split Excel sheets
python -m xlschema split_xlsx [OPTIONS] FILE

# Generate SQLAlchemy from database
python -m xlschema to_sqla [OPTIONS] DATABASE_URI
```

### Core Options

| Option | Description |
|--------|-------------|
| `--format, -f` | Output format(s) to generate |
| `--output, -o` | Output directory (default: `.xlschema/output`) |
| `--models-only` | Generate only model definitions (no data) |
| `--table, -t` | Specific table(s) to process |
| `--sql, -s` | Custom SQL query for data extraction |
| `--clean, -c` | Clean output directory before generation |
| `--run, -r` | Auto-run with population and testing |

---

## Supported Formats

### SQL Dialects
- `sql/postgres` - PostgreSQL with enums and constraints
- `sql/sqlite` - SQLite with appropriate type mappings
- `sql/pgenum` - PostgreSQL enum definitions
- `sql/pgschema` - PostgreSQL schema with relationships
- `sql/pgtap` - PostgreSQL TAP testing framework

### Python Frameworks
- `py/django` - Django model definitions
- `py/djmodels` - Django models with relationships
- `py/djadmin` - Django admin configurations
- `py/djfactories` - Factory Boy test factories
- `py/djserializers` - Django REST Framework serializers
- `py/sqlalchemy` - SQLAlchemy 2.0 models
- `py/pandas` - Pandas DataFrame operations
- `py/psycopg` - Direct psycopg2 operations

### Other Languages
- `java/hibernate` - Java Hibernate entities
- `scala/hibernate` - Scala Hibernate entities
- `hs/model` - Haskell data types
- `hs/persist` - Haskell Persistent models
- `hs/schema` - Haskell schema definitions

### Documentation & Data
- `rst/sphinx` - Sphinx documentation
- `rmd/rmarkdown` - R Markdown reports
- `csv/multi` - Multi-table CSV export
- `xlsx/validation` - Excel validation templates
- `yml/yaml` - YAML schema export

---

## Configuration

### Environment Variables

```bash
# Database connection
export DBI_URI="postgresql://user:pass@host/database"

# Output customization
export XLSCHEMA_OUTPUT="./models"
export XLSCHEMA_PREFIX="app_"
```

### Configuration File (`.xlschema/config.yml`)

```yaml
output_dir: "./generated"
template_dir: "./custom_templates"
default_formats:
  - py/django
  - sql/postgres
field_mappings:
  custom_type: "VARCHAR(255)"
```

---

## Architecture

XLSchema follows a clean **Reader → Schema → Writer** architecture:

### Core Components

1. **Readers** (`src/xlschema/readers/`)
   - `YamlToModel` - YAML file parsing
   - `ExcelToModel` - Excel (.xlsx) file parsing
   - `DBToModel` - Database schema introspection
   - `SqlToModel` - Custom SQL query execution

2. **Schema Model** (`src/xlschema/models.py`)
   - `Schema` - Container for models and enums
   - `Model` - Table/entity definitions with fields and relationships
   - `Enum` - Enumeration type definitions
   - `Field` - Column definitions with types and constraints

3. **Writers** (`src/xlschema/writers/`)
   - Template-based code generation using Mako
   - Format-specific field type mappings
   - Inheritance hierarchy for shared functionality

4. **Plugin System** (`src/xlschema/plugins/`)
   - Extensible command-line interface
   - `CorePlugin` - Main `from_uri` functionality
   - `DisplayPlugin` - Format discovery
   - Custom plugin support

---

## Security Features

XLSchema implements enterprise-grade security measures:

### Input Validation
- **Path Validation**: Prevents directory traversal attacks
- **URI Validation**: Validates database connection strings
- **SQL Injection Prevention**: Query analysis and pattern detection
- **Template Security**: Safe context validation for code generation

### Secure Command Execution
- **subprocess.run()**: Replaces unsafe `os.system()` calls
- **Command Validation**: Input sanitization with `shlex.split()`
- **Timeout Protection**: Prevents hanging processes
- **Error Handling**: Graceful failure handling

### Template Rendering
- **Context Filtering**: Prevents code injection in templates
- **Type Validation**: Strict type checking for template variables
- **Resource Limits**: Memory and processing constraints

---

## Recent Updates

### Version 0.3.15 (Latest)

**Major Upgrades**
- **SQLAlchemy 2.0.43**: Complete migration from 1.4.x with modern async support
- **Python 3.12+**: Updated minimum Python version requirement
- **UV Package Manager**: Migrated from rye to uv for faster dependency resolution

**Security Enhancements**
- Comprehensive input validation for all user inputs
- Secure subprocess execution replacing `os.system()` calls
- Template rendering security with context validation
- SQL injection prevention with query analysis

**Bug Fixes**
- Fixed deprecation warnings from SQLAlchemy 1.4
- Improved error handling with proper exception hierarchies
- Enhanced template compatibility with modern Python

**Performance Improvements**
- Faster database introspection with SQLAlchemy 2.0
- Optimized template rendering pipeline
- Reduced memory footprint for large schemas

---

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Install** development dependencies: `uv sync --dev`
4. **Make** your changes with tests
5. **Run** quality checks: `uv run make check`
6. **Submit** a pull request

### Code Standards

- **Python 3.12+** compatibility
- **Type hints** for all public APIs
- **Comprehensive tests** with pytest
- **Security-first** approach
- **Documentation** for new features

---

## Documentation

- **[User Guide](docs/userguide.rst)** - Comprehensive usage documentation
- **[API Reference](docs/api/)** - Complete API documentation
- **[Developer Guide](docs/devguide.rst)** - Contributing and architecture
- **[CLAUDE.md](CLAUDE.md)** - AI assistant integration guide
- **[Examples](examples/)** - Real-world usage examples

### Building Documentation

```bash
# HTML documentation
uv run make html

# PDF documentation
uv run make pdf

# API documentation
uv run make api
```

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## Acknowledgments

- **SQLAlchemy Team** - For the excellent ORM framework
- **Mako** - For the powerful templating engine
- **Contributors** - Everyone who has contributed to this project
