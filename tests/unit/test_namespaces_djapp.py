import os

from conftest import (
    OPTIONS_DEFAULT, OUTPUT,
    get_app, exists
)

def test_djangoapp_pkg():
    app = get_app('node_props.yml')
    app.write('pkg/djapp')


def test_writer_py_django(prop_app):
#     # prop_app.write('py/django')
    prop_app.write()
#     assert exists('acme')
#     assert exists('acme/person')
#     assert exists('acme/vehicle')
#     assert exists('acme/person_vehicle')

def test_djangoapp_app():
    app = get_app('node_props.yml')
    writer = app.get_writer('pkg/djapp')
    nspace = writer.schema.models[0].nspace
    assert nspace.to_dict
    assert nspace.to_yaml
