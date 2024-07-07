import os

import pytest

from conftest import (
    OUTPUT, OPTIONS_DEFAULT_MAKO, METHODS, METHODS_PROPS,
    exists, check, get_app, cleanup
)

METHODS_ERROR = [
    'hs/model',
    'hs/schema',
]

def get_mako_app(filename='node.yml'):
    app = get_app(filename, options=OPTIONS_DEFAULT_MAKO)
    return app


# GENERAL WRITER TESTS
# ----------------------------------------------------------------------
def test_writer_mako_engine_multi():
    app = get_mako_app()
    app.write('sql/pgschema')
    check('schema/tables/node.sql')
    check('schema/fixtures/node.sql')
    cleanup()

def test_writer_mako_engine_single():
    app = get_mako_app()
    app.write('sql/sqlite')
    check('node_sqlite.sql')

def test_writer_mako_java_hibernate():
    app = get_mako_app('node_props.yml')
    app.write('java/hibernate')
    check('Node.java')

def test_writer_mako_scala_hibernate():
    app = get_app('node_props.yml', options=OPTIONS_DEFAULT_MAKO)
    app.write('scala/hibernate')
    check('Node.scala')

def test_writer_mako_sql_pgenum():
    app = get_mako_app()
    app.write('sql/pgenum')
    check('node_pgenum.sql')

def test_writer_mako_sql_postgres():
    app = get_mako_app()
    app.write('sql/postgres')
    check('node_postgres.sql')

def test_writer_mako_py_sqlalchemy():
    app = get_mako_app()
    app.write('py/sqlalchemy')
    check('node_sqlalchemy.py')

def test_writer_mako_r_data():
    app = get_mako_app()
    app.write('r/data')
    check('node_data.r')

def test_writer_mako_yml_yaml():
    app = get_mako_app()
    app.write('yml/yaml')
    check('node_yaml.yml')

def test_mako_templates_node():
    app = get_mako_app()
    for method in METHODS:
        app.write(method)
    cleanup()

def test_mako_templates_node_props():
    app = get_mako_app('node_props.yml')
    for method in METHODS_PROPS:
        app.write(method)
    cleanup()
