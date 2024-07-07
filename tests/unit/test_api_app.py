import pytest

import xlschema
from conftest import (
    SCHEMA_YAML, METHODS,
    exists, dir_exists, get_app, cleanup, check, app_check, to_output
)

def test_xlschema_import():
    try:
        import xlschema
        assert xlschema.__version__ is not None
    except ImportError as exc:
        assert False, exc

def test_xlschema_app_write_to_sql():
    app_check('node.yml', 'sql/sqlite')

def test_xlschema_app_write_to_xlsx():
    app_check('node.yml', 'xlsx/validation')

def test_xlschema_app_write_to_dir_sql():
    app = get_app('node.yml')
    dir_out = 'schema_out'
    app.write('sql/pgschema', to_path=to_output(dir_out))
    dir_exists(dir_out)

def test_xlschema_app_write_to_dir_hs():
    app = get_app('node.yml')
    dir_out = 'hs_out'
    app.write('hs/model', to_path=to_output(dir_out))
    dir_exists(dir_out)

def test_xlschema_app(app):
    assert len(app.schema.models) > 0
    assert len(app.schema.enums)  > 0
    assert len(app.schema.types)  > 0

def test_app_run_all(app):
    app.run(*METHODS)
    assert exists('schema_sqlite.sql')

def test_app_populate(app):
    app.write('sql/sqlite')
    app.populate('sql/sqlite')
    check('schema_sqlite.sql')

def test_app_writers_property(app):
    writers1 = app.writers
    writers2 = app.writers
    assert writers1[0] is writers2[0]

def test_app_dispatch_continue(app):
    writer_types = ['not/found', 'yml/yaml']
    app.write(*writer_types)
    check('schema_yaml.yml')

def test_app_get_converter_options(app):
    reader = app.get_reader(SCHEMA_YAML, options=None)
    assert reader

def test_app_get_writer_error(app):
    assert not app.get_writer('not/found')

def test_app_error():
    with pytest.raises(xlschema.XLSchemaError):
        app = get_app('./README.md')
