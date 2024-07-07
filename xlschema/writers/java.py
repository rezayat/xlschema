"""Writer classes for JVM languages.

Inheritance structure::

    SchemaWriter
        TemplateWriter
            MultiTemplateWriter
                JavaWriter
                ScalaWriter
"""


from .. import fields
from ..config import register
from .abstract import MultiTemplateWriter


@register
class JavaWriter(MultiTemplateWriter):
    """Java code generator."""

    # model_class = models.JavaModel
    field_class = fields.JavaField
    file_suffix = 'java'
    method = 'hibernate'


@register
class ScalaWriter(MultiTemplateWriter):
    """Scala code generator."""

    # model_class = models.ScalaModel
    field_class = fields.ScalaField
    file_suffix = 'scala'
    method = 'hibernate'
