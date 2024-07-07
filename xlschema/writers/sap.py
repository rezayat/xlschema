"""Writer classes for SAP languages.

Inheritance structure::

    SchemaWriter
        TemplateWriter
            AbapWriter
"""

from .. import fields
from ..config import register
from .abstract import TemplateWriter


@register
class AbapWriter(TemplateWriter):
    """Abap code generator."""

    field_class = fields.AbapField
    file_suffix = 'abap'
    method = 'oo'
