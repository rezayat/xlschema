"""Field classes for the Haskell Language.

Inheritance structure::

    Field
        HaskellField
"""

from ..common.text import Text
from .abstract import Field


class HaskellField(Field):
    """Field type to be used in haskell code generation."""

    TYPES = {
        'str': 'String',        # specified size text
        'txt': 'String',        # arbitrary size text
        'date': 'Date',         # date
        'time': 'POSIXTime',    # Time (CHECK)
        'interval': 'DiffTime',  # Time (CHECK)
        'bool': 'Bool',         # binary
        'int': 'Int',           # int4
        'serial': 'Int',        # int4
        'dec': 'Double',        # single precision floating point
        'float': 'Double',      # double precision floating point
        'double': 'Double',     # double precision floating point
        'numeric': 'Double',    # double precision floating point
    }

    @property
    def name(self):
        """Sets Record field name convention.

        The default is the typical ``modelFieldName`` style. This can be
        switched off by writing ``noprefix`` in the action field.
        """
        if self.action == 'noprefix':
            return Text(self._name).under_to_mixed()
        return Text("{}_{}".format(self.model.name,
                                   self._name)).under_to_mixed()

    @property
    def required_qualifier(self):
        """Required qualifies to handle null values.

        A field which may have a null value is necessarily of type Maybe a
        in Haskell. For example: Maybe Int or Maybe String.
        """
        return 'Maybe'

    @property
    def definition(self):
        """Definition assigment in Haskell.

        Uses patterns from packages:
            - ``postgresql-orm``
            - ``postgres-simple``
        """
        name_len = len(self.name) + 1
        if self.is_pk:
            _type = Text('DBKey')
        elif self.is_enum:
            _type = self._name.classname
        else:
            _type = self.type
        if not self.is_required:
            _type = self.required_qualifier + ' ' + _type
        return '{}{}:: {}'.format(self.name, (30 - name_len) * " ", _type)
