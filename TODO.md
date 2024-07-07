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
