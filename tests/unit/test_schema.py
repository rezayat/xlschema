import pytest

from conftest import OPTIONS_DEFAULT

from xlschema.fields import Field
from xlschema.fields.sql import SqlField
from xlschema.models import Enum, Model, Schema, Namespace


@pytest.fixture(scope="function")
def schema():
    f1 = Field.from_dict(name='name', type='str')
    f2 = Field.from_dict(dict(name='age', type='int'))
    m1 = Model(name='m1', fields=[f1, f2])
    e1 = Enum(name='e1')
    yield Schema(name='sa', models=[m1], enums=[e1])

def test_schema_types(schema):
    assert 'int' in schema.dtypes

def test_schema_specialize(schema):
    schema = schema.specialize(
        schema,
        Model,
        Namespace,
        SqlField,
        OPTIONS_DEFAULT)
    for model in schema.models:
        for field in model.fields:
            assert isinstance(field, SqlField)

def test_schema_not_specialize(schema):
    for model in schema.models:
        for field in model.fields:
            assert not isinstance(field, SqlField)
