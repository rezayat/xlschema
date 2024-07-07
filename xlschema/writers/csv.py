"""Writer classes for CSV.

Inheritance structure::

    SchemaWriter
        TemplateWriter
            MultiTemplateWriter
                CsvWriter
"""
import csv

from .. import fields
from ..config import register
from .abstract import MultiTemplateWriter


@register
class CsvWriter(MultiTemplateWriter):
    """Csv file generator."""

    field_class = fields.Field
    file_suffix = 'csv'
    method = 'multi'

    def write(self, to_path=None):
        """Overriden write method writes 1 model to 1 file in root path."""
        for model in self.schema.models:
            path = self._get_path(model.name.mixed_to_under(), to_path)
            with open(path, 'w', newline='') as target:
                writer = csv.writer(target)
                writer.writerows(model.data)

    def run(self):
        """Default run method."""
        self.write()
