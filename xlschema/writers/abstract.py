"""Abstract Writer classes.

All concrete Field classes must inherit from the appropriate
abstract ``Writer`` class in this module::

    SchemaWriter
        TemplateWriter
            MultiTemplateWriter
"""

import logging
import os

from .. import fields, models
from ..common.mixins import CommandMixin
from ..common.templating import TemplateEngine
from ..config import Config

# ----------------------------------------------------------
# WRITERS
# ----------------------------------------------------------


class SchemaWriter(CommandMixin):
    """Abstract base class for rendering code generation templates to a file.

    Should be subclassed with ``model_class``, ``field_class``,
    ``file_suffix``, and ``method`` specified.
    """

    model_class = models.Model
    nspace_class = models.Namespace
    field_class = fields.Field
    file_suffix = ''
    method = ''

    def __init__(self, schema, options=None):
        """Class constructor.

        :param schema: populated model instances
        :type schema: :py:class:`xlschema.models.Schema`
        """
        self.schema = schema.specialize(schema,
                                        self.model_class,
                                        self.nspace_class,
                                        self.field_class,
                                        options)
        self.options = options
        self.config = Config()
        self.n_args = len(Config.METAFIELDS)
        self.engine = TemplateEngine(templates=str(Config.TEMPLATES),
                                     output=self.options.output)
        self.log = logging.getLogger(self.__class__.__name__)

    @property
    def path(self):
        """Returns a target path for the writer."""
        _path = '{}_{}.{}'.format(self.schema.name,
                                  self.method,
                                  self.file_suffix)
        return os.path.join(self.options.output, _path)

    @property
    def type(self):
        """Returns the type of the writer.

        Ths writer_type is constructed as follows::

            <file_suffix>/<method>

        """
        return "{}/{}".format(self.file_suffix, self.method)

    @property
    def imports(self):
        """Returns a list of model classnames to import."""
        return ', '.join(model.classname for model in self.schema.models)

    def run(self):
        """Default run method."""
        self.write()

    def write(self, to_path=None):
        """Core workhorse method.

        Should be overriden in case different write patterns are
        required.
        """


class TemplateWriter(SchemaWriter):
    """Uses templates to write models to code formats."""

    template = ''

    def render(self, **kwds):
        """Generic mako template renderer."""
        kwds.update(dict(data=self))
        self.log.debug('rendering: %s', self.schema.name)
        if not self.template:
            self.template = '{ext}/{method}.{ext}'.format(
                ext=self.file_suffix, method=self.method)
        template = self.config.TEMPLATE_ENV.get_template(self.template)
        return str(template.render(**kwds))

    def write(self, to_path=None):
        """Basic template to file writer.

        Should be overriden in case different write patterns are
        required.
        """
        if to_path:
            path = to_path
        else:
            path = self.path
        with open(path, 'w') as target:
            self.log.info("writing: %s", path)
            target.write(self.render())


class MultiTemplateWriter(TemplateWriter):
    """Uses templates to write multiple models to code formats."""

    def _get_path(self, name, to_path=None):
        """Return full path of target."""
        _path = '{}.{}'.format(name, self.file_suffix)
        if to_path:
            output = to_path
        else:
            output = self.options.output
        if not os.path.exists(output):
            os.makedirs(output)
        path = os.path.join(output, _path)
        self.log.info("writing: %s", path)
        return path

    def write(self, to_path=None):
        """Overriden write method writes 1 model to 1 file in root path."""
        for model in self.schema.models:
            path = self._get_path(model.name.classname, to_path)
            with open(path, 'w') as target:
                target.write(self.render(model=model, is_model_template=True))
