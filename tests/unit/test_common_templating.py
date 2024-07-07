import pytest

from conftest import (
    TEMPLATES_DIR, OUTPUT, OPTIONS_DEFAULT,
    exists, get_app, check, cleanup, check_template
)

from xlschema.common.templating import (
    Template, TemplateEntry, TemplateEngine)

ENTRY_IS_ABBREV_SHALLOW = 'sql/test'
ENTRY_IS_ABBREV_DEEP = 'py/dj/hello'
ENTRY_IS_FILE = 'sql/pgdir/sqlite.sql'
ENTRY_IS_DIR = 'sql/pgdir'
ENTRY_IS_PKG = 'pkg/djapp'
ENTRY_IS_ERROR = 'foo/bar'

@pytest.fixture(scope="module")
def engine():
    yield TemplateEngine(templates=TEMPLATES_DIR, output=OUTPUT)
    cleanup()

EXPECT_RENDERED = 'hello WORLD\n'

def test_engine_error(engine):
    with pytest.raises(NotImplementedError):
        engine.render(ENTRY_IS_ERROR, world='WORLD')

def test_engine_render_from_abbrev_shallow(engine):
    engine.render(ENTRY_IS_ABBREV_SHALLOW, world='WORLD')
    assert check_template('sql/test.sql', EXPECT_RENDERED)

def test_engine_render_from_abbrev_deep(engine):
    engine.render(ENTRY_IS_ABBREV_DEEP, world='WORLD')
    assert check_template('py/dj/hello.py', EXPECT_RENDERED)

def test_engine_render_from_file(engine):
    engine.render(ENTRY_IS_FILE, world='WORLD')
    assert check_template('sql/pgdir/sqlite.sql', EXPECT_RENDERED)

def test_engine_render_from_dir(engine):
    engine.render(ENTRY_IS_DIR, world='WORLD')
    assert check_template('sql/pgdir/deep/postgres.sql', EXPECT_RENDERED)
    assert check_template('sql/pgdir/sqlite.sql', EXPECT_RENDERED)

def test_engine_render_from_pkg(engine):
    app = get_app('node_props.yml')
    writer = app.get_writer(ENTRY_IS_PKG)
    engine.render(ENTRY_IS_PKG, world='WORLD')
    assert check_template('pkg/djapp/app/__init__.py', EXPECT_RENDERED)
    assert check_template('pkg/djapp/templates/base_app.html', EXPECT_RENDERED)

def test_engine_render_from_string(engine):
    rendered = engine.render_template_from_string(
        'hello ${world}\n', world='WORLD')
    assert rendered == EXPECT_RENDERED

def test_engine_render_from_lookup(engine):
    rendered = engine.render_template_from_lookup(
        'sql/test.sql', world='WORLD')
    assert rendered == EXPECT_RENDERED

def test_template_entry_cases():
    case = lambda entry: TemplateEntry(entry, root=TEMPLATES_DIR)

    assert case(ENTRY_IS_ABBREV_SHALLOW).is_abbrev
    assert case(ENTRY_IS_ABBREV_DEEP).is_abbrev
    assert case(ENTRY_IS_FILE).is_file
    assert case(ENTRY_IS_DIR).is_dir
    assert case(ENTRY_IS_PKG).is_pkg

def test_template_minimal():
    t = Template("hello, ${name}!")
    assert t.render(name="jack") == "hello, jack!"

def test_template_properties():
    from xlschema.common.text import Text
    t = Template("hello, ${name.classname}!")
    assert t.render(name=Text("foo_bar")) == "hello, FooBar!"

def test_template_implicit_function_calls():
    from xlschema.common.text import Text
    t = Template("hello, ${name.strip_id()}!")
    assert t.render(name=Text("foo_id")) == "hello, foo!"

def test_engine_hashed(engine):
    rendered = engine.render_template_from_string(
        'hello ${world}\n', world='WORLD')
    assert rendered == EXPECT_RENDERED
    assert engine.hashed(rendered) == engine.hashed(EXPECT_RENDERED)

# def test_compare_files():
#     engine = TemplateEngine(root=TEMPLATES_DIR, output=OUTPUT)
#     app = get_app("node_props.yml", options=OPTIONS_DEFAULT)
#     writer = app.get_writer('py/djrestviews')
#     nspace = writer.schema.models[0].nspace
#     engine.render_templates(**nspace.to_dict)
