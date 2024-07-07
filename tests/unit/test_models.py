import os
import pytest

from conftest import get_app, OUTPUT

import xlschema

join = lambda *paths: os.path.join(*(str(p) for p in paths))


def test_model_person(app):
    model = app.schema.models[0]

    assert model.name == 'person'
    assert len(model.required_fields) == 4

    # field assertions
    assert not model.has_defaults
    assert not model.has_actions

    # test primary key fields
    assert model.has_pk
    assert model.pk_field.name == 'id'
    assert len(model.pk_fields) == 1

    # indexing assertions
    assert not model.has_fk
    assert not model.has_composite_keys
    assert not model.has_pfk

    # rows ops
    row = [1, 'jon', 21, 'A']
    zipped = model.row_zip(row, quote=False)
    assert zipped == [('id', 1), ('name', 'jon'), ('age', 21), ('rating', 'A')]

def test_model_vehicle(app):
    model = app.schema.models[1]
    assert model.name == 'vehicle'
    assert len(model.required_fields) == 7

    # field assertions
    assert model.has_defaults

    # test primary key fields
    assert model.has_pk
    assert model.pk_field.name == 'id'
    assert len(model.pk_fields) == 1

    # test foreign key
    assert model.has_fk

    # test semantic key field
    assert model.has_sk
    assert model.sk_field.name == 'brand'
    assert len(model.sk_fields) == 1

def test_model_person_vehicle(app):
    model = app.schema.models[2]
    assert model.name == 'person_vehicle'
    assert len(model.required_fields) == 5

    # test primary key fields
    assert model.has_pk
    assert model.pk_field.name == 'id'
    assert len(model.pk_fields) == 1

    # test primary foreign key fields
    # because it does not have a pfk field
    assert not model.is_mtm and model.metadata['is_mtm']

def test_enum(app):
    assert len(app.schema.enums) > 0
    enum = app.schema.enums['color']
    assert enum.data[0] == ('blue', 'blue')

def test_model_person_vehicle_m2m(m2mapp):
    model = m2mapp.schema.models[2]
    assert model.name == 'person_vehicle'
    assert len(model.required_fields) == 5

    # test primary foreign key fields
    assert model.has_pfk
    assert len(model.pfk_fields) == 1
    assert model.is_mtm

    # must be a specialized model for definitions
    writer = m2mapp.get_writer('sql/sqlite')
    model = writer.schema.models[2]
    assert model.definitions

def test_model_pfk():
    app = get_app('node_pfk.yml')
    writer = app.get_writer('sql/sqlite')
    node, nodedata = writer.schema.models
    assert node.has_actions
    assert nodedata.has_pfk
    assert nodedata.pfk_definition == 'primary key(node_id)'
    assert nodedata.definitions
    node_id = nodedata.fields[0]
    assert node_id.is_pfk
    assert node_id.definition

def test_model_empty_type_error():
    from xlschema.fields.abstract import FieldError
    with pytest.raises(FieldError):
        app = get_app('node_error.yml')

def test_namespace():
    app = get_app('node_props.yml')
    writer = app.get_writer('sql/sqlite')

    nspace = writer.schema.models[0].nspace

    assert nspace.model == 'app.core.models.Node'
    assert nspace.app == 'app.core'

    assert nspace.model_classname == 'Node'
    assert nspace.app_name == 'core'
    assert repr(nspace) == "<Namespace model:'app.core.models.Node' app:'app.core'>"

    assert nspace.app_level == 2
    assert nspace.model_classname_title == 'Node'
    assert nspace.model_classname_plural == 'Nodes'
    assert nspace.model_classname_plural_title == 'Nodes'

    assert nspace.app_name_plural == 'cores'
    assert nspace.app_parent == 'app'
    assert nspace.app_parent_name == 'app'

    assert nspace.model_parent == 'app.core.models'

    # these are Pathlib.Path instances
    assert str(nspace.path_base) == 'core'
    assert str(nspace.path) == join(OUTPUT, nspace.path_base)
    assert str(nspace.path_parent) == OUTPUT

    # get the dict
    assert nspace.to_dict
