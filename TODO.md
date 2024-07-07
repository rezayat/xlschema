# TO DO

## Primary Tasks:

### Documentation
- [ ] Improve documentation
  - [ ] Improve README.md
  - [ ] Sphinx docs
  - [x] UML docs
  - [ ] Docstrings
  - [ ] Doctests
  - [ ] Type Hinting / Annotations

### API Improvements

Differentiate between type of the template and the type of the writer. Right now they are one and the same.

Allow for ability to over-ride the class variable with a instance variable of template. Where do you specify the template and then when is it specialized (Field, Namespace). Should consider a different model.

- [ ] Change API
  - [ ] API: change `Xlschema` API
    - [ ] write(writer_type, template, to_path)
  - [ ] Commandline:
    - [ ] Change `--format` to `--writer`
    - [ ] Add `--template`
  - [ ] `GenericWriter` and `GenericMultiWriter`: include `TemplateEngine` logic as a fallback in case an specialized writer class is not available.
- [ ] Introduce concept of a `Recipe`
- [ ] `transformer` functions: `Schema -> Schema`
- [ ] Provide for ``.write(to_path)`` for custom output paths
  - [x] API support
  - [ ] Commandline support

  #### Schema Validation

- [ ] Add schema validation
  - [ ] see [schema](https://pypi.python.org/pypi/schema/0.6.6), a library for validating Python data structures, such as those obtained from config-files, forms, external services or command-line parsing, converted from JSON/YAML (or something else) to Python data-types.
  - [ ] see [schematics](https://pypi.python.org/pypi/schematics) Schematics is a Python library to combine types into structures, validate them, and transform the shapes of your data based on simple descriptions.



### Plugins
- [ ] Add XLFormatter: takes an excel table and converts it to XLSX Specfile format

## Secondary Tasks:

### Packaging
- [ ] Improve packaging infrastructure
  - [ ] `python3 setup.py test` corrupts `data/db/test.sqlite` (fix)

### Extensibility
- [ ] Allow for local customization
  - [x] Plugins to add writers, fields, and templates
  - [ ] Tasks with DAG-like dependencies resolution
  - [x] User or Project-level template directories (``.xlschema/templates``)

### Dependencies
  - [ ] Evaluate Mako templating (in lieu of jinja2 and cheetah)

### Core
- [ ] Examine using sqlalchemy internal model as a part of core.

### Django
- [ ] Add django test generation (via faker)

- [ ] Pending django fixes
  - [ ] Test correctness of generation.
  - [x] Generates apps to different directories
  - [ ] Generate django fixtures in yaml or json
  - [ ] Omit id column to make it automatic
  - [ ] Add verbose_name

### External Libraries
- [ ] Look at other libraries:
  - [cement](http://builtoncement.com) generic and mature cli framework with many similarities to xlschema
  - [tmpld](https://github.com/joeblackwaslike/tmpld): Jinja2 templating on steroids for docker containers.
  - [Brownbat](https://github.com/DouglasRaillard/BrownBat): Lazy Code Generation
  - [Fashion](https://github.com/braddillman/fashion): Simple model transformation and source code generation
  - [srcgen](https://github.com/tomerfiliba/srcgen): semantic code generation framework
  - [Dagger](https://github.com/trustyou/dagger): performs tasks, providing you with parallel execution, and dependency resolution.
  - [parse_type](https://github.com/jenisys/parse_type): parse_type extends the parse module (opposite of string.format())
  - [yasha](https://github.com/kblomqvist/yasha): Yasha is a code generator based on Jinja2 template engine.
  - [python-docx-template](https://github.com/elapouya/python-docx-template): Use a docx as a jinja2 template
  - [orderedattrdict](https://pypi.python.org/pypi/orderedattrdict): An ordered dictionary with attribute-style access.
---

# CHANGELOG

### Usability

- [x] set default output folder 'output'
- [x] disable 'app' templates on render all



### Structural Refactoring / Simplification
- [x] Refactoring / Simplification of Architecture:
  - [x] Rename `Converter` to `SchemaReader`
  - [x] Rename `Writer` to `SchemaWriter`
  - [x] `generators.apps.App` -> `models.Namespace`
  - [x] Drop Cheetah
  - [x] Drop Jinja2
  - [x] Drop `Generator`

### Template Unification
- [x] Templating Unification:
  - [x] Mako equivalence to Jinja2
  - [x] Drop (jinja2, cheetah) -> Mako

### Code Quality
- [x] 100% Test Coverage
- [x] Perfect pylint 10:10
- [x] Radon: 'A' maintainability score
- [x] No complaints from flake8
- [x] No complaints from proselint
- [x] Appliy isort to all python files

### Dependencies
- [x] Drop `easydict`

### API

- [x] Moved prefix command-line options to global

- [x] Add sensible defaults to options for Library API access (see config below).

- [x] Add ``**kwds`` to ``XLSchema`` class.

- [x] Investigate introducing a `Schema` class to the application which would hold models, enums, and metadata. A `Schema` class is consumed by `SchemaReader` and `Writer` classes.

- [x] Convert `argparse.Namespace` variable `options` into `vars(options)` dict in `Xlschema` class.

- [x] Revise and simplify API
  - [x] Drop `from_db` and `from_file` subcommands and use `from_uri`
  - [x] removed `xlschema.common.cmdline` in `__main__`-> argparse main function which can be extended by plugins (argparse cmd, templates, writer, field, etc.)
  - [x] Spin off splitter into a plugin

- [x] Add plugin system (commandline-oriented)

- [x] Environment variables are now properly picked up in config

- [x] Minimal fields YAML uris

- [x] Metafield reordering: swap places with `description` and `action`

- [x] Make xlschema yaml configurable

### Configuration
- [x] Minimize global configuration (delete all refs to Config.OUTPUT)
- [x] Configuration values should be read from local ``.config.yml``
  - [x] Include logging configuration

### Tests
- [x] Centralize paths in tests to ``conftests.py``
- [x] Move test files from ``./data/*`` to ``tests/data/*``
- [x] Improve test coverage (currently 100%)
- [x] Create/improve testing using pytest
  - [x] Refactored tests
  - [x] Added test for splitter
  - [x] Added test for DBToExcel
  - [x] Add test for sqlacodegen
  - [x] Add test for django app generator
  - [x] Add test for depends

### Writers
- [x] Add django factories for test generation
- [x] Add django rest framework serializers

### Libraries
- [x] Convert to python 3
- [x] Added [Mako](http://www.makotemplates.org) as alternative (potentially core) template library
