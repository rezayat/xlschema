import os

import pytest

from conftest import (
    OUTPUT, METHODS,
    exists, check, get_app,
    cleanup, clean_local_dir)


# GENERAL WRITER TESTS
# ----------------------------------------------------------------------
def test_writer_write():
    app = get_app('node.yml')
    app.write(*METHODS)
    assert exists('node_postgres.sql')
    cleanup()

def test_writer_class(app):
    writer = app.get_writer('sql/sqlite')
    assert writer.type == 'sql/sqlite'
    writer.cmd('echo "Hello World"')
    writer.run()
    check('schema_sqlite.sql')

def test_excel_writer():
    app = get_app('test-no-data.xlsx')
    app.write('xlsx/validation')
    check('test-no-data_validation.xlsx')

def test_writer_pfk():
    app = get_app('node_pfk.yml')
    app.write('py/sqlalchemy')
    check('node_pfk_sqlalchemy.py')
    # tests for 'default'
    app.write('abap/oo')
    check('node_pfk_oo.abap')
    # tests for noprefix action
    app.write('hs/schema')
    check('node_pfk_schema.hs')

def test_writer_person():
    app = get_app('person.yml')
    app.write('py/sqlalchemy')
    check('person_sqlalchemy.py')
    app.write('sql/sqlite')
    check('person_sqlite.sql')

def test_writer_unicode():
    app = get_app('unicode.yml')
    app.write('py/sqlalchemy')
    check('unicode_sqlalchemy.py')

def test_writer_no_output_option():
    app = get_app('node.yml',
        output=None,
        clean=False,
        update_only=False,
        models_only=False)
    assert os.path.exists('./.xlschema/data/README.md')
    app.write('sql/sqlite')
    path = './.xlschema/data/output/node_sqlite.sql'
    assert os.path.exists(path)
    clean_local_dir()

# SPECIALIZED WRITER TESTS
# ----------------------------------------------------------------------
def test_writer_abap_oo(app):
    app.write('abap/oo')
    check('schema_oo.abap')

def test_writer_hs_model(app):
    app.write('hs/model')
    check('Person.hs')
    check('PersonVehicle.hs')
    check('Vehicle.hs')

def test_writer_hs_persist(app):
    app.write('hs/persist')
    check('schema_persist.hs')

def test_writer_hs_schema(app):
    app.write('hs/schema')
    check('schema_schema.hs')

def test_writer_java_hibernate(prop_app):
    prop_app.write('java/hibernate')
    check('Person.java')
    check('PersonVehicle.java')
    check('Vehicle.java')

# def test_writer_py_django(prop_app):
#     # prop_app.write('py/django')
#     prop_app.write()
#     assert exists('acme')
#     assert exists('acme/person')
#     assert exists('acme/vehicle')
#     assert exists('acme/person_vehicle')

def test_writer_py_djadmin(app):
    app.write('py/djadmin')
    check('schema_djadmin.py')

def test_writer_py_djfactories(app):
    app.write('py/djfactories')
    check('schema_djfactories.py')

def test_writer_py_djfactories_props():
    app = get_app('node_props.yml')
    app.write('py/djfactories')
    check('node_props_djfactories.py')

def test_writer_py_djfactorytests():
    app = get_app('node_props.yml')
    app.write('py/djfactorytests')
    check('node_props_djfactorytests.py')

def test_writer_py_djmodels(app):
    app.write('py/djmodels')
    check('schema_djmodels.py')

def test_writer_py_djrestviews(prop_app):
    prop_app.write('py/djrestviews')
    check('django_djrestviews.py')

def test_writer_py_djserializers(app):
    app.write('py/djserializers')
    check('schema_djserializers.py')

def test_writer_py_pandas(app):
    app.write('py/pandas')
    check('schema_pandas.py')

def test_writer_py_psycopg(app):
    app.write('py/psycopg')
    check('schema_psycopg.py')

def test_xlschema_py_records(app):
    app.write('py/records')
    check('schema_records.py')

def test_xlschema_py_sqlalchemy(app):
    app.write('py/sqlalchemy')
    check('schema_sqlalchemy.py')

def test_xlschema_r_data(app):
    writer = app.get_writer('r/data')
    writer.run()
    check('schema_data.r')

def test_xlschema_rmd_rmarkdown(app):
    writer = app.get_writer('rmd/rmarkdown')
    writer.run()
    check('schema_rmarkdown.rmd')

def test_xlschema_rst_sphinx(app):
    app.write('rst/sphinx')
    check('schema_sphinx.rst')

def test_xlschema_scala_hibernate(prop_app):
    prop_app.write('scala/hibernate')
    check('Person.scala')
    check('PersonVehicle.scala')
    check('Vehicle.scala')

def test_xlschema_sql_pgenum(app):
    app.write('sql/pgenum')
    check('schema_pgenum.sql')

def test_xlschema_sql_pgschema(app):
    app.write('sql/pgschema')
    check('schema/tables/person.sql')
    check('schema/fixtures/person.sql')
    check('schema/tables/vehicle.sql')
    check('schema/fixtures/vehicle.sql')
    check('schema/tables/person_vehicle.sql')
    check('schema/fixtures/person_vehicle.sql')

def test_xlschema_sql_pgtap(app):
    writer = app.get_writer('sql/pgtap')
    writer.run() # write(), test()
    check('schema_pgtap.sql')

def test_xlschema_sql_postgres(app):
    writer = app.get_writer('sql/postgres')
    writer.write()
    check('schema_postgres.sql')
    writer.populate()

def test_xlschema_sql_sqlite(app):
    app.write('sql/sqlite')
    check('schema_sqlite.sql')

def test_xlschema_xlsx_validation(app):
    app.write('xlsx/validation')
    check('schema_validation.xlsx')

def test_xlschema_yml_yaml(app):
    writer = app.get_writer('yml/yaml')
    writer.run()
    check('schema_yaml.yml')
