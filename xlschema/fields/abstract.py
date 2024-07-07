"""Abstract Field Classes.

All concrete Field classes must inherit from the abstract `Field` class
in this module::

    Field
    FieldError(Exception)

"""

from ..common.text import Text
from ..common.utils import is_number
from ..config import Config


# ----------------------------------------------------------
# FIELD EXCEPTIONS
# ----------------------------------------------------------
class FieldError(Exception):
    """Indicates an error in the specification of fields."""

# ----------------------------------------------------------
# FIELD TYPES
# ----------------------------------------------------------


class Field:
    """Base abstract class for all field types."""

    VALID_TYPES = [
        'serial',
        'str', 'txt',
        'date', 'time', 'interval',
        'bool',
        'int',
        'dec', 'float', 'double', 'numeric',
    ]
    TYPES = {key: key for key in VALID_TYPES}
    METAFIELDS = Config.METAFIELDS

    def __init__(self, name, ftype, length, index, required,
                 default, constraint, category, action, description, options=None):
        """Field constructor (order is important)."""
        self._name = Text(name)
        self._type = Text(ftype)
        self.length = int(length) if length else length
        self.index = index
        self._required = int(required) if required else required
        self._default = Text.wrap(default) if not is_number(default) else default
        self.constraint = Text.wrap(constraint)
        self.category = Text.wrap(category)
        self.action = Text.wrap(action)
        self.description = Text.wrap(description)
        # to be set by parent
        self.options = options
        self._model_name = None
        self.model = None
        self.is_last = False

    def __repr__(self):
        return "<{} '{}.{}' ({})>".format(
            self.__class__.__name__, self.model_name, self.name, self.type)

    def format(self, fstring, *args, **kwargs):
        """Helper function to improve readability of formatted strings.

        It does this by checking attributes automatically from self
        """
        # for conveniences f -> field so as to do {f.name}
        kwargs['f'] = self
        return Text.wrap(fstring.format(*args, **kwargs))

    @classmethod
    def from_dict(cls, dikt=None, **kwds):
        """Helper classmethod to create fields from a dict (k,v)."""
        spec = {f: None for f in cls.METAFIELDS}
        if dikt:
            spec.update(dikt)
        if kwds:
            spec.update(kwds)
        # assert dikt['name'], 'required metafield name value missing'
        # assert dikt['type'], 'required metafield type value missing'
        return cls(*tuple([spec[f] for f in reversed(cls.METAFIELDS)]))

    @property
    def offset(self):
        """Returns the rjust offset from the leftmost definition.

        This is used, for example, to justify comments.
        """
        return self.model.config.TEMPLATE_COMMENT_OFFSET

    @property
    def model_name(self):
        """Retrieves and caches the model_name from the parent model."""
        if not self._model_name and not self.model:
            self._model_name = Text('model')
        if self.model and not self._model_name:
            self._model_name = self.model.name
        return self._model_name

    def values(self):
        """Field metadata values as a tuple."""
        return (self.name,
                self.type,
                self.length,
                self.index,
                self.required,
                self.default,
                self.constraint,
                self.category,
                self.action,
                self.description)

    @property
    def name(self):
        """Field name to be overriden in case of changes."""
        return self._name

    @property
    def fname(self):
        """Field name which should never be overriden."""
        return self._name

    def _typecheck(self):
        """Checks type of field and sets its value from appropriate sources."""
        if not self._type or self._type == 'None':
            raise FieldError('Field type is not specified',
                             "{}.{}".format(self.model_name, self.name))
        if self._type == 'str':
            if self.length:
                _type = self.TYPES[self._type].format(self.length)
            else:
                _type = self.TYPES['txt']
        else:
            # print self._name, self._type
            _type = self.TYPES[self._type]
        return _type

    @property
    def type(self):
        """Public Field type which can/should be overridden."""
        return self._typecheck()

    @property
    def ftype(self):
        """Field type (never to be overriden!)."""
        return self._type

    @property
    def default(self):
        """Returns a calculated default value in the respective language."""
        return self._default

    @property
    def comma(self):
        """Comma prop for adding comma at end of line."""
        if self.is_last:
            return ''
        return ','

    @property
    def required(self):
        """Field is required."""
        return self._required

    @property
    def definition(self):
        """Field definition property (must be overriden)."""
        raise NotImplementedError

    @property
    def is_key(self) -> bool:
        """Field is a primary key, foreign key, or both.

        Note: the exclusion of sk keys test
        """
        return self.index in ['pk', 'fk', 'pfk']

    @property
    def is_pk(self) -> bool:
        """Field is a primary key."""
        return self.index == 'pk'

    @property
    def is_fk(self) -> bool:
        """Field is a foreign key."""
        return self.index == 'fk'

    @property
    def is_self_referential(self) -> bool:
        """Field is a foreign key and has the name 'parent_id'."""
        return self.is_fk and (self.fname == 'parent_id')

    @property
    def is_pfk(self) -> bool:
        """Field is a primary foreign key.

        These are only used in one-to-one relationships
        """
        return self.index == 'pfk'

    @property
    def is_sk(self) -> bool:
        """Field is a semantic key. (i.e meaningful for humans).

        These are used to indicate that the field should text-searchable.
        """
        return self.index == 'sk'

    @property
    def is_enum(self) -> bool:
        """Field has an enum type."""
        if self.constraint:
            return self.constraint.startswith('enum')
        return False

    @property
    def is_required(self) -> bool:
        """Field is required."""
        return self._required == 1

    @property
    def is_number(self) -> bool:
        """Field is of a number type."""
        return self._type in ['int', 'dec', 'float', 'double', 'numeric']
