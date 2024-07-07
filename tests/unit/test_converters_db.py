import sqlalchemy
import pytest
from conftest import OPTIONS_SQL, OPTIONS_TABLE, TEST_DB, check, sql, populate_db
from xlschema.readers.db import DBToModel, SqlToModel


def test_sqlmodel_get_types():
    fieldnames = ('id', 'savings', 'name', 'to_date', 'person_id')
    row = (1, 1.0, 'hello', '2016-10-12', 1)
    expected_types = ['int', 'float', 'str', 'date', 'int']
    assert SqlToModel.get_types(row, fieldnames) == expected_types

def test_db_to_model():
    app = DBToModel(TEST_DB, options=OPTIONS_TABLE)
    assert len(app.schema.models) > 0
    assert len(app.schema.types)  > 0

def test_sql_to_model(populate_db):
    app = SqlToModel(TEST_DB, options=OPTIONS_SQL)
    assert len(app.schema.models) > 0
    assert len(app.schema.types)  > 0

def test_sql_to_model_error():
    with pytest.raises(sqlalchemy.exc.OperationalError):
        app = SqlToModel(TEST_DB, options=sql(
            'select * from notable'
        ))

def test_write_from_dbapp(dbapp):
    dbapp.write('sql/sqlite')
    check('test_sqlite.sql')

def test_write_from_sqlapp(sqlapp):
    sqlapp.write('sql/sqlite')
    check('test_sqlite.sql')
