# CHANGELOG


## v0.2x


## v0.1

### Usability

- set default output folder 'output'
- disable 'app' templates on render all



### Structural Refactoring / Simplification
- Refactoring / Simplification of Architecture:
  - Rename `Converter` to `SchemaReader`
  - Rename `Writer` to `SchemaWriter`
  - `generators.apps.App` -> `models.Namespace`
  - Drop Cheetah
  - Drop Jinja2
  - Drop `Generator`

### Template Unification
- Templating Unification:
  - Mako equivalence to Jinja2
  - Drop (jinja2, cheetah) -> Mako

### Code Quality
- 100% Test Coverage
- Perfect pylint 10:10
- Radon: 'A' maintainability score
- No complaints from flake8
- No complaints from proselint
- Appliy isort to all python files

### Dependencies
- Drop `easydict`

### API

- Moved prefix command-line options to global

- Add sensible defaults to options for Library API access (see config below).

- Add ``**kwds`` to ``XLSchema`` class.

- Investigate introducing a `Schema` class to the application which would hold models, enums, and metadata. A `Schema` class is consumed by `SchemaReader` and `Writer` classes.

- Convert `argparse.Namespace` variable `options` into `vars(options)` dict in `Xlschema` class.

- Revise and simplify API
  - Drop `from_db` and `from_file` subcommands and use `from_uri`
  - removed `xlschema.common.cmdline` in `__main__`-> argparse main function which can be extended by plugins (argparse cmd, templates, writer, field, etc.)
  - Spin off splitter into a plugin

- Add plugin system (commandline-oriented)

- Environment variables are now properly picked up in config

- Minimal fields YAML uris

- Metafield reordering: swap places with `description` and `action`

- Make xlschema yaml configurable

### Configuration
- Minimize global configuration (delete all refs to Config.OUTPUT)
- Configuration values should be read from local ``.config.yml``
  - Include logging configuration

### Tests
- Centralize paths in tests to ``conftests.py``
- Move test files from ``./data/*`` to ``tests/data/*``
- Improve test coverage (currently 100%)
- Create/improve testing using pytest
  - Refactored tests
  - Added test for splitter
  - Added test for DBToExcel
  - Add test for sqlacodegen
  - Add test for django app generator
  - Add test for depends

### Writers
- Add django factories for test generation
- Add django rest framework serializers

### Libraries
- Convert to python 3
- Added [Mako](http://www.makotemplates.org) as alternative (potentially core) template library
