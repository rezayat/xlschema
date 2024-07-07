"""Writer classes for Django libraries and frameworks.

Inheritance structure::

    SchemaWriter
        TemplateWriter
            SqlWriter
                PythonWriter
                    DjangoFactoriesWriter
                    DjangoWriter
                        DjangoModelsWriter
                        DjangoAdminWriter
                        DjangoFactoryTestsWriter
                        DjangoSerializerWriter
                        DjangoRestViewsWriter
"""


from .. import fields
from ..config import register
from ..namespaces import DjangoApp
from .python import PythonWriter


class DjangoWriter(PythonWriter):
    """Generic writer for django."""

    field_class = fields.DjangoField

    def run(self):
        """Default run method."""
        self.write()


@register
class DjangoModelsWriter(DjangoWriter):
    """Rudimentary writer for django models.

    TODO: provide feature for data inserts
    """

    method = 'djmodels'


@register
class DjangoAdminWriter(DjangoWriter):
    """Rudimentary writer for django admins."""

    method = 'djadmin'


# @register
# class DjangoTestsWriter(DjangoWriter):
#     """Rudimentary writer for django tests.
#     """
#     method = 'djtests'


@register
class DjangoFactoriesWriter(PythonWriter):
    """FactoryBoy ``factories.py`` file writer."""

    field_class = fields.FactoryBoyField
    method = 'djfactories'


@register
class DjangoFactoryTestsWriter(DjangoWriter):
    """Tests based on FactoryBoy ``factories.py``."""

    method = 'djfactorytests'


@register
class DjangoSerializerWriter(DjangoWriter):
    """Django Rest Framework Serializer writer."""

    method = 'djserializers'


@register
class DjangoRestViewsWriter(DjangoWriter):
    """Django Rest Framework Views writer."""

    method = 'djrestviews'


@register
class DjangoAppWriter(PythonWriter):
    """Rudimentary writer for django apps."""

    nspace_class = DjangoApp
    file_suffix = 'pkg'
    method = 'djapp'

    def write(self, to_path=None):
        """Default write method."""
        self.log.info('type: %s', self.type)
        for model in self.schema.models:
            if model.has_app_model_properties:
                self.log.debug('model.name = %s', model.name)
                self.log.debug('model.nspace.app_name: %s', model.nspace.app_name)
                self.engine.render(self.type, model=model)
                # self.engine.render(self.type, **model.nspace.to_dict)
