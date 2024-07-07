import pytest

from conftest import (
    XLSCHEMA, FROM_URI, OUTPUT,
    SCHEMA_XLSX, SCHEMA_YAML, DJANGO_YAML,
    TEST_DB, METHODS,
    shell, exists, check,
    populate_db,
)

# can be skipped with: pytest -k-slow
pytestmark = pytest.mark.slow()

def test_xlschema():
    shell([XLSCHEMA])

def test_xlschema_output():
    shell([XLSCHEMA,
           '--output', OUTPUT])

def test_xlschema_from_uri_empty():
    shell([FROM_URI])

def test_xlschema_from_uri_xlsx_methods():
    shell([FROM_URI, SCHEMA_XLSX, '--format'] + METHODS)
    check('schema_sqlite.sql')

def test_xlschema_from_uri_yaml_methods():
    shell([FROM_URI, SCHEMA_YAML, '--format'] + METHODS)
    check('schema_sqlite.sql')

def test_xlschema_from_uri_sqlite_xlsx_populate():
    shell([FROM_URI, SCHEMA_YAML,
           '--populate',
           '--format'] + METHODS)
    check('schema_sqlite.sql')

def test_xlschema_from_uri_sqlite_xlsx_run():
    shell([FROM_URI, '-f sql/sqlite',
          '--run', SCHEMA_XLSX])
    check('schema_sqlite.sql')

def test_xlschema_from_uri_run_all():
    shell([FROM_URI, DJANGO_YAML, '--run'])
    check('django_sqlite.sql')

def test_xlschema_from_uri_write_all():
    shell([FROM_URI, DJANGO_YAML])
    check('django_sqlite.sql')

def test_xlschema_xlsx_from_uri_xlsx_run_methods():
    shell([FROM_URI, SCHEMA_XLSX,
           '--run',
           '--format'] + METHODS)
    check('schema_sqlite.sql')

def test_xlschema_from_uri_xlsx_options():
    shell([XLSCHEMA,
           '--output', OUTPUT,
           '--clean',
           'from_uri',
           SCHEMA_XLSX,
           '--run',
           '--populate',
           '--format', 'sql/sqlite'])
    check('schema_sqlite.sql')

def test_xlschema_from_uri_db_sql(populate_db):
    shell([XLSCHEMA,
           '--output', OUTPUT,
           '--prefix test',
           'from_uri',
           TEST_DB,
           '--sql "select * from person"',
           '--format', 'sql/sqlite'])
    check('test_sqlite.sql')

def test_xlschema_from_uri_db_tables(populate_db):
    shell([XLSCHEMA,
           '--output', OUTPUT,
           '--prefix test',
           'from_uri',
           TEST_DB,
           '--table person vehicle person_vehicle',
           '--format', 'sql/sqlite'])
    check('test_sqlite.sql')

def test_xlschema_from_uri_db_tables_no_prefix():
    shell([XLSCHEMA,
           '--output', OUTPUT,
           'from_uri',
           TEST_DB,
           '--table person',
           '--format', 'sql/sqlite'])
