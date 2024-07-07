import pytest

from xlschema import fields

FIELD_CASES = {
    #name, ftype, length, index, required, default, constraint, category, action, description, options=None)
'pk-normal':
    ('id',   'int', None, 'pk',  True,     None,    None,       None,     None,   "primary key", None),

'str-nolength':
    ('name', 'str', None, 'pk',  False,    'sam',   None,       None,     None,   None, None),

'error-notype':
    ('name', None, None, 'pk',  False,    'sam',   None,       None,     None,   None, None),
}

def test_model_person(app):
    model = app.schema.models[0]
    assert model.name == 'person'
    fields = model.fields
    field = fields[0]
    assert field.name == 'id'
    assert field.fname == 'id'
    assert field.format('{f.name}') == 'id'
    assert field.default == ''
    assert field.is_pk
    assert field.is_key
    assert not field.is_sk
    assert field.model.name == 'person'
    assert field.model_name == 'person'
    assert repr(field) == "<Field 'person.id' (int)>"

def test_abstract_field_definition_notimplemented():
    with pytest.raises(NotImplementedError):
        f = fields.Field(*FIELD_CASES['pk-normal'])
        definition = f.definition

def test_abstract_field_no_offset():
    class TestField(fields.PostgresField):
        @property
        def offset(self):
            return 0
    f = TestField(*FIELD_CASES['pk-normal'])
    assert f.definition == 'id integer primary key not null,'

def test_django_field_nolength():
    f = fields.DjangoField(*FIELD_CASES['str-nolength'])
    assert f.definition == 'name = models.TextField(blank=False, null=False, primary_key=True)'

def test_pgenum_field_nolength():
    f = fields.PgEnumField(*FIELD_CASES['str-nolength'])
    assert f.ftype == 'str'
    assert f.type == 'text'

def test_pgenum_field_error_notype():
    with pytest.raises(fields.abstract.FieldError):
        f = fields.PgEnumField(*FIELD_CASES['error-notype'])
        type = f.type
