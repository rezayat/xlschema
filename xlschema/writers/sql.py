"""Writer classes for SQL dialects.

Inheritance structure::

    SchemaWriter
        TemplateWriter
            SqlWriter
                PostgresWriter
                    PostgresMultiWriter
                    PgEnumWriter
                    PgTapWriter
                SqliteWriter
"""


import datetime
import os

from .. import fields
from ..common.text import Text
from ..config import register
from .abstract import TemplateWriter


class SqlWriter(TemplateWriter):
    """Abstract Superclass which is meant to be subclassed by other writers."""

    file_suffix = 'sql'
    method = 'sql'

    def run(self):
        """Default run method."""
        self.write()
        self.populate()

    def populate(self):
        """Populate DB."""

    def process(self, row):
        """Use for cell operations during inserts in sql (postgres, sqlite)."""
        def _cell(value):
            """Used to transform individual elements during data inserts."""
            # pylint: disable=too-many-return-statements
            # try:
            if value in [None, 'n/a', '']:
                return 'null'
            elif isinstance(value, str):
                if self.options.clean:
                    return Text(value).clean()
                return value
            elif isinstance(value, int):
                return value
            elif isinstance(value, datetime.datetime):
                return str(value)
            elif isinstance(value, datetime.date):
                return str(value)
            else:
                return value
            # except UnicodeEncodeError as err:
                # self.log.exception('Error: %s: %s', err, row)

        return str(tuple(_cell(i) for i in row)).replace("'null'", 'null')


@register
class PostgresWriter(SqlWriter):
    """Postgres specific writer."""

    field_class = fields.PostgresField
    method = 'postgres'

    def populate(self):
        """Load postgresql file directly into database."""
        self.log.debug('populating: %s', self.path)
        self.cmd('psql -f {}', self.path)

    def process(self, row):
        """Use for postgres row by row copy operations."""
        # print row
        return '\t'.join(tuple(str(i) for i in row)).replace('None', r'\N')


@register
class PostgresMultiWriter(PostgresWriter):
    """Postgres specific writer to multiple files."""

    field_class = fields.PostgresField
    method = 'pgschema'

    def render(self, **kwds):
        """Generic mako template renderer."""
        method = kwds.get('method')
        # if method:
        #     del kwds['method']
        kwds.update(dict(data=self))
        self.log.debug('rendering: %s', self.schema.name)
        tmpl_name = '{ext}/{method}.{ext}'.format(
            ext=self.file_suffix, method=method)
        template = self.config.TEMPLATE_ENV.get_template(tmpl_name)
        return str(template.render(**kwds))

    def write(self, to_path=None):
        """Overriden write method writes 1 model to 1 file in root path."""
        if to_path:
            output = to_path
        else:
            output = self.options.output
        schema = os.path.join(output, 'schema')
        tables = os.path.join(schema, 'tables')
        fixtures = os.path.join(schema, 'fixtures')
        subdirs = [schema, tables, fixtures]
        for subdir in subdirs:
            try:
                os.makedirs(subdir)
            except OSError:
                continue

        # make tables & fixtures
        for model in self.schema.models:
            _path = '{}.{}'.format(model.name, self.file_suffix)
            table = os.path.join(tables, _path)
            fixture = os.path.join(fixtures, _path)
            self.log.debug("writing: %s", table)
            with open(table, 'w') as t_target:
                rendered = self.render(
                    method='pgtable', model=model, is_model_template=True)
                t_target.write(rendered)
            if model.data:
                self.log.debug("writing: %s", fixture)
                with open(fixture, 'w') as f_target:
                    rendered = self.render(
                        method='pgdata', model=model, is_model_template=True)
                    f_target.write(rendered)


@register
class PgEnumWriter(PostgresWriter):
    """Postgres writer with native enum support."""

    field_class = fields.PgEnumField
    method = 'pgenum'


@register
class PgTapWriter(PostgresWriter):
    """PgTap code generator."""

    file_suffix = 'sql'
    method = 'pgtap'

    def test(self):
        """Run test."""
        self.log.debug('testing %s', self.path)
        self.cmd('pg_prove {}', self.path)

    def run(self):
        """Default run method."""
        self.write()
        self.test()


@register
class SqliteWriter(SqlWriter):
    """Sqlite specific writer."""

    field_class = fields.SqliteField
    method = 'sqlite'

    def populate(self):
        """Populate into sqlite db."""
        self.log.debug('populating: %s', self.path)
        sqlite_db = os.path.join(self.options.output,
                                 '{}_{}.db'.format(self.schema.name,
                                                   self.method))
        self.cmd('sqlite3 {} < {}', sqlite_db, self.path)
