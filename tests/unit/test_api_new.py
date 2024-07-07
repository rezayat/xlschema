import pytest

from xlschema.config import Config
from xlschema.common.templating import TemplateEngine

from conftest import (OPTIONS_DEFAULT, TEMPLATES_DIR, OUTPUT,
                      get_app, check_template, check)


ENTRY_IS_ABBREV_SHALLOW = 'sql/test'
ENTRY_IS_ABBREV_DEEP = 'py/dj/hello'
ENTRY_IS_FILE = 'sql/pgdir/sqlite.sql'
ENTRY_IS_DIR = 'sql/pgdir'
ENTRY_IS_PKG = 'pkg/djapp'
ENTRY_IS_ERROR = 'foo/bar'

def write_schema(app, entry):
    config = Config()
    try:
        writer = config.WRITERS[entry](app.schema, OPTIONS_DEFAULT)
        writer.write()
    except KeyError:
        engine = TemplateEngine(TEMPLATES_DIR, OUTPUT)
        engine.render(entry, schema=app.schema)

def write_engine_writer(app, entry):
    config = Config()
    writer = PGWriter(app.schema, OPTIONS_DEFAULT)
    writer.write()

def test_config_writer_types():
    config = Config()
    writer_types = sorted(config.WRITERS)
    # print(writer_types)
    assert len(writer_types) > 10

def test_config_writer_render_options(app):
    write_schema(app, 'sql/sqlite')
    check('schema_sqlite.sql')

def test_config_writer_render_options(app):
    write_schema(app, 'sql/schema.sql')
    assert check_template('sql/schema.sql', "person\nvehicle\nperson_vehicle\n")

def test_config_writer_render_options_app():
    app = get_app('schema.yml', options=OPTIONS_DEFAULT)
    write_schema(app, 'sql/schema.sql')
    assert check_template('sql/schema.sql', "person\nvehicle\nperson_vehicle\n")
