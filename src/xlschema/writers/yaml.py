"""Writer classes for YAML.

Inheritance structure::

    SchemaWriter
        TemplateWriter
            YamlWriter
"""

import yaml

from .. import fields
from ..config import register
from .abstract import TemplateWriter


@register
class YamlWriter(TemplateWriter):
    """Yaml code generator."""

    field_class = fields.Field
    file_suffix = 'yml'
    method = 'yaml'

    def run(self):
        """Default run method."""
        self.write()
        self.validate()

    def validate(self):
        """Validate yaml using pyyaml."""
        self.log.debug('validating and rewriting %s', self.path)
        with open(self.path) as fopen:
            yml = yaml.load(stream=fopen, Loader=yaml.SafeLoader)
        with open(self.path, 'w') as fwrite:
            yaml.dump(yml, stream=fwrite, default_flow_style=False)
