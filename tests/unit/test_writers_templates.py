import pytest

from conftest import (
    OPTIONS_DEFAULT, OPTIONS_DEFAULT_MAKO, METHODS, METHODS_PROPS,
    get_app, exists, check, cleanup
)

METHODS_ERROR = [
    'hs/model',
    'hs/schema',
]

@pytest.fixture(scope="module", params=[OPTIONS_DEFAULT,
                                        OPTIONS_DEFAULT_MAKO])
def node_app(request):
    app = get_app('node.yml', options=request.param)
    yield app
    cleanup()

@pytest.fixture(scope="module", params=[OPTIONS_DEFAULT,
                                        OPTIONS_DEFAULT_MAKO])
def node_props_app(request):
    app = get_app('node_props.yml', options=request.param)
    yield app
    cleanup()


@pytest.fixture(scope="module", params=METHODS)
def dual_node_app(request):
    specfile = 'node.yml'
    jinja2_app = get_app(specfile, options=OPTIONS_DEFAULT)
    mako_app = get_app(specfile, options=OPTIONS_DEFAULT_MAKO)
    yield (jinja2_app, mako_app)
    cleanup()

@pytest.fixture(scope="module", params=METHODS_PROPS)
def dual_node_props_app(request):
    specfile = 'node_props.yml'
    jinja2_app = get_app(specfile, options=OPTIONS_DEFAULT)
    mako_app = get_app(specfile, options=OPTIONS_DEFAULT_MAKO)
    yield (jinja2_app, mako_app)
    cleanup()

# GENERAL WRITER TESTS
# ----------------------------------------------------------------------
def test_writers_templates_node(node_app):
    for method in METHODS:
        node_app.write(method)

def test_writers_templates_node_props(node_props_app):
    for method in METHODS_PROPS:
        node_props_app.write(method)

def test_writers_templates_dual_node(dual_node_app):
    jinja2_app, mako_app = dual_node_app
    for method in METHODS:
        jinja2_app.write(method)
        mako_app.write(method)

def test_writers_templates_dual_node_props(dual_node_props_app):
    jinja2_app, mako_app = dual_node_props_app
    for method in METHODS_PROPS:
        jinja2_app.write(method)
        mako_app.write(method)
