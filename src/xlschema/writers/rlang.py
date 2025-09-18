"""Writer classes for the R languages and its derivatives.

Inheritance structure::

    SchemaWriter
        TemplateWriter
            RlangWriter
            RMarkdownWriter
"""

from .. import fields
from ..config import register
from .abstract import TemplateWriter


@register
class RMarkdownWriter(TemplateWriter):
    """Rmarkdown report writer."""

    field_class = fields.PostgresField
    file_suffix = 'rmd'
    method = 'rmarkdown'

    def run(self):
        """Default run method."""
        self.write()
        self.report()

    def report(self):
        """Render report from code."""
        self.log.debug('rendering to report %s', self.path)
        self.cmd('renderRmd {}', self.path, fail_ok=True)


@register
class RlangWriter(TemplateWriter):
    """Rlanguage writer."""

    field_class = fields.PostgresField
    file_suffix = 'r'
    method = 'data'

    def run(self):
        """Default run method."""
        self.write()
        self.report()

    def report(self):
        """Render report from code."""
        self.log.debug('rendering to report %s', self.path)
        self.cmd('renderRmd {}', self.path, fail_ok=True)
