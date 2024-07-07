"""Documentation-oriented Writer classes.

Writer classes for documentation languages::

    SchemaWriter
        TemplateWriter
            RstSchemaWriter
"""

from .. import fields
from ..config import register
from .abstract import TemplateWriter


@register
class RstSchemaWriter(TemplateWriter):
    """Restructured text writer."""

    field_class = fields.PostgresField
    file_suffix = 'rst'
    method = 'sphinx'
