"""General On-Demand Import Manager for Packages.

Solves the problem of only importing classes on
demand given a unique key.

"""
import abc
import importlib
from collections import OrderedDict


class ImportManagerError(Exception):
    """General exception class."""


class ImportManager(abc.ABC):
    """Abstract on-demand class import manager.

    Expects a ``library`` and/or an ``class_index``
    parameter in the following formats::

        library = {
            '<package>': ['<classname>'],
        }


        class_index = {
            '<key>': '<package>.<classname>',
        }

    For example::

        library = {
            'sql': ['SqlWriter', 'PostgresWriter'],
        }

        class_index = {
            'sql/sqlite': 'sql.SqlWriter',
        }
    """

    context = None  # must be initialized as __name__ in subclass

    def __init__(self, library=None, class_index=None):
        """Initialize ImportManager.

        :param library: dictionary of package / classes
        :type library: dict

        :param class_index: dictionary of key: pgk.classname
        :type class_index: Dict[str, str]
        """
        self.library = library
        self.classes, self.class_index = self._setup(library, class_index)

    @abc.abstractmethod
    def gen_key(self, cls):
        """Generates a unique key for the class index.

        Override this with your customer key-generating function.

        For example::
                return cls.__name__
        """

    def _setup(self, library, class_index=None):
        """Conditionally returns an odict of classes and dict index."""
        if class_index:
            # lazy mode: don't load classes and build index
            return (OrderedDict(), class_index)

        if library:
            _classes = OrderedDict()
            _class_index = {}
            for pkg in library:
                class_names = library[pkg]
                module = importlib.import_module('.' + pkg, self.context)
                for class_name in class_names:
                    cls = getattr(module, class_name)
                    key = self.gen_key(cls)
                    _classes[key] = cls
                    _class_index[key] = '{}.{}'.format(pkg, class_name)
            return (_classes, _class_index)
        else:
            raise ImportManagerError("Must provide a library or a class_index.")

    def get_class(self, key):
        """Key-based class retrieval."""
        pkg, classname = self.class_index[key].split('.')
        module = importlib.import_module('.' + pkg, self.context)
        return getattr(module, classname)
