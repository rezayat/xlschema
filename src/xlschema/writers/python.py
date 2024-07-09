"""Writer classes for Python libraries and frameworks.

Inheritance structure::

    SchemaWriter
        TemplateWriter
            SqlWriter
                PythonWriter
                    PsycopgWriter
                    SqlAlchemyWriter
                    RecordsWriter
                    PandasWriter
"""


from .. import fields
from ..config import register
from .sql import SqlWriter


class PythonWriter(SqlWriter):
    """Abstract class for holding python specific writing behaviour."""

    file_suffix = 'py'

    def populate(self):
        """Populate from python."""
        self.log.debug('populating: %s', self.path)
        self.cmd('python {}', self.path)


@register
class PsycopgWriter(PythonWriter):
    """Writer to generate psycopg python code from models."""

    field_class = fields.PostgresField
    method = 'psycopg'


@register
class SqlAlchemyWriter(PythonWriter):
    """Writer to produce sqlalchemy models from xl."""

    field_class = fields.SqlAlchemyField
    method = 'sqlalchemy'


@register
class RecordsWriter(PythonWriter):
    """Writer to produce ``records`` handles."""

    field_class = fields.SqlAlchemyField
    method = 'records'


@register
class PandasWriter(PythonWriter):
    """Writer to produce ``pandas`` dataframes."""

    field_class = fields.SqlAlchemyField
    method = 'pandas'
