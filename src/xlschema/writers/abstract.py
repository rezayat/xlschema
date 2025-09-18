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
        """Generic mako template renderer with security validation."""
        from ..common.exceptions import TemplateRenderingError

        # Validate template context
        safe_kwds = self._validate_template_context(kwds)
        safe_kwds.update(dict(data=self))

        self.log.debug('rendering: %s', self.schema.name)

        # Validate template name
        if not self.template:
            self.template = '{ext}/{method}.{ext}'.format(
                ext=self.file_suffix, method=self.method)

        validated_template = self._validate_template_name(self.template)

        try:
            template = self.config.TEMPLATE_ENV.get_template(validated_template)
            return str(template.render(**safe_kwds))
        except Exception as e:
            error_msg = f"Template rendering failed: {e}"
            self.log.error(error_msg)
            raise TemplateRenderingError(
                error_msg,
                template_name=validated_template,
                context_keys=list(safe_kwds.keys())
            )

    def _validate_template_name(self, template_name: str) -> str:
        """Validate template name for security.

        :param template_name: template name to validate
        :returns: validated template name
        :raises TemplateRenderingError: if template name is invalid
        """
        import re
        from ..common.exceptions import TemplateRenderingError

        if not template_name or not isinstance(template_name, str):
            raise TemplateRenderingError("Template name must be a non-empty string")

        # Check for path traversal attempts
        if '..' in template_name or template_name.startswith('/'):
            raise TemplateRenderingError(f"Template name contains path traversal: {template_name}")

        # Check for valid template name pattern
        if not re.match(r'^[a-zA-Z0-9_/.-]+$', template_name):
            raise TemplateRenderingError(f"Template name contains invalid characters: {template_name}")

        # Limit template name length
        if len(template_name) > 255:
            raise TemplateRenderingError("Template name too long (max 255 chars)")

        return template_name

    def _validate_template_context(self, context: dict) -> dict:
        """Validate template context data for security.

        :param context: template context dictionary
        :returns: validated context dictionary
        :raises TemplateRenderingError: if context is invalid
        """
        from ..common.exceptions import TemplateRenderingError

        if not isinstance(context, dict):
            raise TemplateRenderingError("Template context must be a dictionary")

        # Limit context size
        if len(context) > 1000:
            raise TemplateRenderingError("Template context too large (max 1000 keys)")

        safe_context = {}
        dangerous_keys = {'__builtins__', '__globals__', '__locals__', 'exec', 'eval', 'open', '__import__'}

        for key, value in context.items():
            # Validate key
            if not isinstance(key, str):
                self.log.warning("Skipping non-string key in template context: %s", key)
                continue

            if key in dangerous_keys or key.startswith('_'):
                self.log.warning("Skipping potentially dangerous context key: %s", key)
                continue

            # Basic value validation
            if self._is_safe_template_value(value):
                safe_context[key] = value
            else:
                self.log.warning("Skipping potentially dangerous context value for key: %s", key)

        return safe_context

    def _is_safe_template_value(self, value) -> bool:
        """Check if a value is safe for template rendering.

        :param value: value to check
        :returns: True if value is safe
        """
        # Allow basic types
        safe_types = (str, int, float, bool, list, dict, tuple, type(None))

        if type(value) in safe_types:
            # For collections, recursively check contents
            if isinstance(value, (list, tuple)):
                return all(self._is_safe_template_value(item) for item in value)
            elif isinstance(value, dict):
                return all(
                    isinstance(k, str) and self._is_safe_template_value(v)
                    for k, v in value.items()
                )
            return True

        # Allow specific xlschema model classes
        if hasattr(value, '__class__'):
            class_name = value.__class__.__name__
            safe_classes = {'Schema', 'Model', 'Enum', 'Field', 'Text'}
            if class_name in safe_classes:
                return True

        return False

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
