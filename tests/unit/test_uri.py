import os

import pytest
import sqlalchemy

import xlschema.uri
from conftest import (POSTGRES_DB, SCHEMA_XLSX, SCHEMA_YAML, TEMPLATE_XLSX,
                      TEST_DB)
from xlschema.config import Config


def test_parse():
    empty = TEMPLATE_XLSX
    paths = [
        (SCHEMA_XLSX,   'xlsx',        None),
        (SCHEMA_YAML,   'yaml',        None),
        (TEST_DB,       'database',    'sqlite'),
        (POSTGRES_DB,   'database',    'postgresql'),
        (empty,         None,          None),
    ]
    for path, expected, db_type in paths:
        parser = xlschema.uri.URIParser(path)
        assert parser.type == expected
        assert parser.db_type == db_type
        if parser.db_type in ['postgresql']:
            assert parser.is_db_uri
            assert parser.name == 'db'
        if parser.db_type in ['sqlite']:
            assert parser.name == 'test'
        if parser.type in ['yaml']:
            assert parser.is_yaml
            assert parser.name == 'schema'
        if parser.type in ['xlsx']:
            assert parser.is_xlsx
            assert parser.name == 'schema'
