"""Writer classes for Haskell libraries and frameworks.

The inheritance structure of these classes is as follows::

    ModelWriter
        TemplateWriter
            HaskellWriter
                HaskellSchemaWriter
                HaskellPersistWriter

            MultiTemplateWriter
                HaskellModelWriter

"""

from .. import fields
from ..config import register
from .abstract import MultiTemplateWriter, TemplateWriter


class HaskellWriter(TemplateWriter):
    """Generic Haskell language writer."""

    field_class = fields.HaskellField
    file_suffix = 'hs'


@register
class HaskellSchemaWriter(HaskellWriter):
    """Single-file Writer class for Haskell ORMs.

    This class combines features from the following package
    to provide typesafe mapping between haskell and sql domains:

    - postgresql-simple

    - postgresql-orm

    This template creates 1 file per schema
    """

    method = 'schema'
    template = 'hs/pgorm.hs'


@register
class HaskellModelWriter(MultiTemplateWriter):
    """Multi-file Writer class for Haskell ORMs.

    This class combines features from the following package
    to provide typesafe mapping between haskell and sql domains:

    - postgresql-simple

    - postgresql-orm

    This template creates 1 file per model
    """

    field_class = fields.HaskellField
    file_suffix = 'hs'
    method = 'model'
    template = 'hs/pgorm.hs'


@register
class HaskellPersistWriter(HaskellWriter):
    """Alternative haskell writer using the persistent orm.

    This provides typesafe mapping between haskell and sql domains
    and creates creates 1 file per schema.
    """

    method = 'persist'
