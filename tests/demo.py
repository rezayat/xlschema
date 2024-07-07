from conftest import *
# ============================================================================
import pytest

from xlschema.config import Config, register
from xlschema.common.templating import TemplateEngine

def write_schema(app, entry):
    config = Config()
    try:
        writer = config.WRITERS[entry](app.schema, OPTIONS_DEFAULT)
        writer.write()
    except KeyError:
        engine = TemplateEngine(TEMPLATES_DIR, OUTPUT)
        engine.render(entry, data=app)

def test_write_schema():
    ENTRY_IS_ABBREV_SHALLOW = 'sql/sqlite'

    entries = [
        ENTRY_IS_ABBREV_SHALLOW,
    ]

    app = get_app('schema.yml', options=OPTIONS_DEFAULT)
    schema = app.schema
    for entry in entries:
        write_schema(app, entry)

ENTRY_IS_ABBREV_SHALLOW = 'sql/test'
ENTRY_IS_ABBREV_DEEP = 'py/dj/hello'
ENTRY_IS_FILE = 'sql/pgdir/sqlite.sql'
ENTRY_IS_DIR = 'sql/pgdir'
ENTRY_IS_PKG = 'pkg/djapp'
ENTRY_IS_ERROR = 'foo/bar'

params = {
    # template              # writer_type
    # <partial_path>        # <file_suffix>/<namespace/method>
    #
    'sql/sqlite.sql':       'sql/sqlite',
    'sql/pgdir/sqlite.sql': 'sql/sqlite',
    'py/django/model.py':   'py/django/model',

}

def render_templates(uri, writer_types, templates, to_paths, options=None, **kwds): pass

# single template (what about multiples?)
def render_template(uri, writer_type, template=None, to_path=None, options=None, **kwds):
    app = xlschema.XLSchema(uri, options=OPTIONS_DEFAULT)
    app.write(writer_type, options=options, **kwds)
    # app.write(writer_type, template, options=options, **kwds)
    # app.write(writer_type, template, to_path, options=options, **kwds)
    # def write(self, *writer_types, to_path=None)
