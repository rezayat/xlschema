"""Module for core datamodel of xlschema.

These classes provide the principal mapping abstractions which facilitate
translation from one language or framework to another::

    Object
        Schema
            Model
            Enum
            Namespace
"""
import logging
from collections import OrderedDict
from pathlib import Path

import yaml

from .common.list import List
from .common.text import Text
from .common.utils import is_number
from .config import Config


# ----------------------------------------------------------
# Core Model Classes
# ----------------------------------------------------------
class ObjectMixin:
    """Basic object mixin class."""

    def __repr__(self):
        return "<{} '{}'>".format(self.__class__.__name__, self.name)


class Schema(ObjectMixin):
    """Primary container class of model elements."""

    def __init__(self, name, models=None, enums=None, options=None):
        """Schema constructor.

        :param name: name of the schema instance
        :type name: str

        :param models: list of models in the schema
        :type models: List of :py:class:`xlschema.models.Model`

        :param enums: list of enums in the schema
        :type enums: List of :py:class:`xlschema.models.Enum`

        :param options: argparse options
        :type options: :py:class:`argparse.Namespace`
        """
        self.name = Text(name)
        self.models = models if models else []
        self.enums = enums if enums else {}
        self.options = options
        self.types = set()
        self.metadata = {}
        self.log = logging.getLogger(self.__class__.__name__)
        self.validate()

    @property
    def dtypes(self):
        """Returns set of types used in model fields."""
        return set([f.ftype for model in self.models for f in model.fields])

    @classmethod
    def specialize(cls, schema, model_class, nspace_class, field_class, options):
        """Specializes the model and field classes internally."""
        return cls(
            name=schema.name[:],
            models=[m.clone(model_class, nspace_class, field_class, options)
                    for m in schema.models],
            enums=schema.enums.copy(),
            options=options)

    def validate(self):
        """Check for validation errors."""
        # check for enums
        for m  in self.models:
            for f in m.enum_fields:
                 # assert f.fname in self.enums, f"enum-constrained field '{f.fname}' has no corresponding enum"
                try:
                   assert f.fname in self.enums
                except AssertionError:
                    self.log.critical(f"enum-constrained field '{f.fname}' has no corresponding enum")
                    raise

class Enum(ObjectMixin):
    """Principal class for enum objects which having 2 fields at most."""

    def __init__(self, name, data=None):
        """Class constructor.

        :param name: name of the enumeration
        :type name: str

        :param data: optional key, value rows of data
        :type data: List[(str, str)]
        """
        self.name = Text(name)
        self.data = data  # [EnumRow]
        self.log = logging.getLogger(self.__class__.__name__)
        self.config = Config()

    def keys(self):
        """Returns [k] of [(k,v)]."""
        return [key for (key, _) in self.data]

    def items(self):
        """Returns [(k,v)] items of data where k,v are Text instances."""
        return [(Text(key), Text(val)) for (key, val) in self.data]

    @property
    def type(self) -> str:
        """Returns type of key part of data can only be str or int."""
        return 'str' if isinstance(self.data[0][0], str) else 'int'


class Model(ObjectMixin):
    """Principal class for table model objects having N fields."""

    def __init__(self, name, fields=None, data=None, properties=None,
                 metadata=None, options=None, nspace_class=None):
        """Class constructor.

        :param name: name of the model
        :type name: str

        :param data: list of field instances
        :type data: :py:class:`xlschema.fields.abstract.Field`

        :param data: optional rows of data
        :type data: List[tuple]

        :param properties: optional user visible model properties
        :type properties: dict

        :param metadata: optional system visible model metadata
        :type metadata: dict

        :param options: optional argparse options
        :type options: :py:class:`argparse.Namespace`

        :param nspace_class: optional arbitrary namespace class for customization
        :type nspace_class: python class
        """
        self.name = Text(name)
        self.fields = fields if fields else []
        self.data = data if data else []
        self.properties = properties if properties else OrderedDict()
        self.metadata = metadata if metadata else dict(is_mtm=False)
        self.options = options
        self.nspace = nspace_class(self) if nspace_class else None
        self.log = logging.getLogger(self.__class__.__name__)
        self.config = Config()
        self.setup()  # must be run!

    def _has_field(self, ftype):
        """Check for existance of an index field type."""
        for field in self.fields:
            if field.index == ftype:
                return True
        return False

    def _fields_of_type(self, ftype):
        """Retrieve all instances of an index field type."""
        return [
            f for f in self.fields if f.index == ftype
        ]

    @property
    def is_mtm(self) -> bool:
        """Does an extra check (to see if pfk fields are defined)."""
        return self.metadata['is_mtm'] and self.pfk_fields

    def setup(self):
        """Sets last field .is_last property to True."""
        nfields = len(self.fields)
        for i, field in enumerate(self.fields):
            field.model = self
            if (i == nfields - 1) and (not self.is_mtm):
                field.is_last = True

    def clone(self, model_class, nspace_class, field_class, options):
        """Used to specialize model_classes,field classes."""
        _fields = []
        for field in self.fields:
            _field = field_class(*list(field.values()), options=options)
            _field.model = field.model
            _field.is_last = field.is_last
            _fields.append(_field)
        return model_class(self.name, _fields, self.data, self.properties,
                           self.metadata, options, nspace_class)

    @property
    def fieldnames(self):
        """Returns a list of the model's field names."""
        return [field.name for field in self.fields]

    @property
    def fieldnames_stripped(self):
        """Returns a list of stripped fieldnames.

        Note that foreign key fieldnames are stripped
        of the '_id' part at the end.
        """
        _fields = []
        for field in self.fields:
            if field.is_fk:
                _fields.append(field.name.strip_id())
            else:
                _fields.append(field.name)
        return _fields

    # pylint: disable=no-self-use
    def _quote(self, value):
        """Type specific quotation of values."""
        if value is None:
            return value

        if is_number(value):
            return value

        return '"{}"'.format(value)

    def row_zip(self, row, quote=True):
        """Returns row dict as list."""
        if quote:
            _row = [(field, self._quote(value))
                    for field, value in zip(self.fieldnames, row)]
        else:
            _row = list(zip(self.fieldnames, row))
        return _row

    def row_dict(self, row, sep='=', quote=True):
        """Returns row items as str."""
        _row = ['{}{}{}'.format(key, sep, value)
                for key, value in self.row_zip(row, quote)]
        return ', '.join(_row)

    def row_clean(self, row):
        """Returns a transformed and represented row."""
        noop = lambda x: x

        type_transformers = {
            'str': noop,
            'txt': noop,
            'date': lambda d: str(d).replace(' 00:00:00', ''),
            'time': str,
            'interval': str,
            'bool': bool,
            'int': noop,
            'dec': noop,
            'float': noop,
            'double': noop,
            'numeric': noop,
            'serial': noop,
        }
        funcs = [type_transformers[f.ftype] for f in self.fields]
        return [f(x) for f, x in zip(funcs, row)]

    @property
    def definitions(self):
        """Provides single api to list of all field definitions and extras."""
        _defs = []
        # field definitions
        for field in self.fields:
            _defs.append(field.definition)
        # in case model is many-to-many
        if self.is_mtm:
            _defs.append(self.pfk_definition)
        # anything else
        return _defs

    @property
    def methods(self):
        """Provides single api to list of all method definitions."""
        _methods = []
        # field definitions
        for field in self.fields:
            _methods.append(field.method)
        return _methods

    @property
    def mapped_fields(self):
        """Return all fields except the primary key field."""
        return [
            f for f in self.fields if f.type and f.index != 'pk'
        ]

    @property
    def required_fields(self):
        """Return all required (i.e. not null) fields."""
        return [
            f for f in self.fields if f.required
        ]

    @property
    def pk_field(self):
        """Get primary key field."""
        for field in self.fields:
            if field.index == 'pk':
                return field

    @property
    def pk_fields(self):
        """Return all primary key fields."""
        return self._fields_of_type('pk')

    @property
    def has_pk(self) -> bool:
        """Assert model has primary key field."""
        return self._has_field('pk')

    @property
    def has_fk(self) -> bool:
        """Assert model has at least one foreign key field."""
        return self._has_field('fk')

    @property
    def fk_fields(self):
        """Return all foreign key fields."""
        return self._fields_of_type('fk')

    @property
    def dependencies(self):
        """Return dependencies."""
        _deps = []
        for field in self.fk_fields:
            dep = '--REQ tables/{}'.format(field.name[:-3])
            _deps.append(dep)
        return _deps

    @property
    def has_sk(self) -> bool:
        """Checks if a column is specified as the semantic key for the model.

        Entering 'sk' into the index column sets it as a column which sorts the model
        and organizes the data meaningfully.

        This has various application in data.analysis and distinguishes the column
        as one which can be helpful for humans organizing information.

        So an incrementing integer field is not an sk column (but is typically a primary key),
        whereas the name of an organization or a company name can be an 'sk' column.

        Note that this feature is used in R data.table using the `setkey` function
        """
        return self._has_field('sk')

    @property
    def sk_field(self):
        """Get semantic key field."""
        for field in self.fields:
            if field.index == 'sk':
                return field

    @property
    def sk_fields(self):
        """Return all semantic key fields.

        These are searchable fields
        """
        return self._fields_of_type('sk')

    @property
    def has_composite_keys(self) -> bool:
        """Assert model has > 1 primary key field."""
        return len(self.pk_fields) > 1

    @property
    def has_pfk(self) -> bool:
        """Check if table has a field marked as `pfk`.

        This means that it is at once a primary key field
        and also a foreign key field.
        """
        return self._has_field('pfk')

    @property
    def pfk_fields(self):
        """Return all primary foreign key fields."""
        return self._fields_of_type('pfk')

    @property
    def pfk_definition(self):
        """Returns primary foreign keys."""
        fields = ', '.join(field.name for field in self.pfk_fields)
        return 'primary key({})'.format(fields)

    @property
    def enum_fields(self):
        """Retrieve fields which are specified as enum (in constraints)."""
        return [field for field in self.fields if field.is_enum]

    @property
    def enum_fieldnames(self):
        """Retrieve fieldnames of enum fields."""
        return [field.name for field in self.enum_fields]

    @property
    def category_fields(self):
        """Retrieve field which have category specified."""
        return [field for field in self.fields if field.category]

    @property
    def number_fields(self):
        """Retrieve all number fields."""
        return [field for field in self.fields if field.is_number]

    @property
    def noncategory_fields(self):
        """Retrieve field which have don't have a category specified."""
        return [field for field in self.fields if not field.category]

    @property
    def noncategory_fieldnames(self):
        """Retrieve fieldnames which don't have a category specified."""
        return [field.name for field in self.noncategory_fields]

    @property
    def noncategory_admin_fieldnames(self):
        """Remove `id` and `*_id` from noncategory model fieldnames."""
        _results = []
        for fieldname in self.noncategory_fieldnames:
            if fieldname == 'id':
                continue
            if fieldname.endswith('_id'):
                fieldname = fieldname[:-3]
            _results.append(fieldname)
        return _results

    @property
    def categories(self):
        """Retrieve set of categories."""
        return List.unique([field.category for field in self.category_fields])

    def fields_for_category(self, category):
        """Retrieve fields for a given category."""
        return [field for field in self.fields if field.category == category]

    def fieldnames_for_category(self, category):
        """Retrieve fieldnames for a given category."""
        return [field.name for field in self.fields_for_category(category)]

    @property
    def types(self):
        """Gets list of all types used in the model."""
        return [f.type for f in self.fields]

    @property
    def has_defaults(self) -> bool:
        """Returns True if there are any default fields."""
        for field in self.fields:
            if field.default:
                return True
        return False

    @property
    def has_actions(self) -> bool:
        """Returns True if there are any action fields."""
        for field in self.fields:
            if field.action:
                return True
        return False

    @property
    def is_hierarchical(self) -> bool:
        """Returns True if model is hierarchical (has a parent field)."""
        for field in self.fields:
            if field.name == 'parent_id' and field.is_fk:
                return True
        return False

    @property
    def classname(self):
        """Class name format for names (hello_world -> HelloWorld)."""
        return self.name.classname

    def line(self, symbol='-', txt=None):
        """Generates a line in restructured text and markdown text output."""
        if txt:
            return symbol * (len(self.name) + 1 + len(txt))
        return symbol * len(self.name)

    @property
    def has_app_model_properties(self):
        """Tests whether model.properties have 'app', 'model' defs."""
        return all(p in self.properties for p in ['model', 'app'])


class Namespace:
    """An abstract class which specifies a namespace for code generation."""

    def __init__(self, parent):
        """General constructor.

        :param parent: parent model install
        :type parent: Model

        """
        self.parent = parent
        self._nspace = {}

    def __repr__(self):
        return "<{} model:'{}' app:'{}'>".format(
            self.__class__.__name__, self.model, self.app)

    def _path(self, path):
        """Helper function to conditionally insert root path before path."""
        return self.path_output / path

    @property
    def path_base(self):
        """Returns base path of app."""
        return Path('/'.join(self.app_structure[1:]))

    @property
    def path(self):
        """Returns path of app."""
        return self._path(self.path_base)

    @property
    def path_parent(self):
        """Returns parent of path of app."""
        return self._path('/'.join(self.app_structure[1:][:-1]))

    @property
    def path_output(self):
        """Returns output path from options."""
        return Path(self.parent.options.output)

    @property
    def app(self):
        """Returns the app definition from properties."""
        return Text(self.parent.properties['app'])

    @property
    def app_structure(self):
        """Returns the structural parts of the app."""
        return self.app.split('.')

    @property
    def app_name(self):
        """Returns the name part of the app structure."""
        return Text(self.app_structure[-1:][0])

    @property
    def model(self):
        """Returns model definition from properties."""
        return Text(self.parent.properties['model'])

    @property
    def model_structure(self):
        """Returns model structure."""
        return self.model.split('.')

    @property
    def model_classname(self):
        """Returns name of the app."""
        return Text(self.model_structure[-1:][0])

    @property
    def model_parent(self):
        """Returns parent of model."""
        return '.'.join(self.model_structure[:-1])

    @property
    def model_classname_title(self):
        """Returns title of classname (i.e. with spaces)."""
        return Text(" ".join([word.title()
                              for word in (self.model_classname
                                           .mixed_to_under()
                                           .split('_'))]))

    @property
    def model_classname_plural(self):
        """Return pluralized classname."""
        return self.model_classname.plural()

    @property
    def model_classname_plural_title(self):
        """Return pluralized classname title."""
        return self.model_classname_title.plural()

    @property
    def app_name_plural(self):
        """Returns plural of name."""
        return self.app_name.plural()

    @property
    def app_level(self):
        """Returns depth of nesting."""
        return len(self.app_structure)

    @property
    def app_parent(self):
        """Returns parent of app."""
        return '.'.join(self.app_structure[:-1])

    @property
    def app_parent_name(self):
        """Returns name of parent of app."""
        return self.app_parent.split('.')[-1]

    def update_nspace_core(self, nspace):
        """Updates internal namespace."""
        nspace['app'] = str(self.app)
        nspace['app_name'] = str(self.app_name)
        nspace['app_name_plural'] = str(self.app_name_plural)
        nspace['app_parent'] = str(self.app_parent)
        nspace['app_parent_name'] = str(self.app_parent_name)
        nspace['app_structure'] = self.app_structure
        nspace['app_level'] = self.app_level

        nspace['model'] = str(self.model)
        nspace['model_parent'] = str(self.model_parent)
        nspace['model_classname'] = str(self.model_classname)
        nspace['model_classname_title'] = str(self.model_classname_title)
        nspace['model_classname_plural'] = str(self.model_classname_plural)
        nspace['model_classname_plural_title'] = str(self.model_classname_plural_title)
        nspace['model_structure'] = self.model_structure

        nspace['path'] = str(self.path)
        nspace['path_base'] = str(self.path_base)
        nspace['path_parent'] = str(self.path_parent)
        nspace['path_output'] = str(self.path_output)

    @property
    def to_dict(self):
        """Returns a dict of key attributes."""
        nspace = self._nspace

        # update core attributes
        self.update_nspace_core(nspace)

        return nspace

    @property
    def to_yaml(self):
        """Return yaml version of .to_dict attributes."""
        return yaml.dump(self.to_dict, default_flow_style=False)
