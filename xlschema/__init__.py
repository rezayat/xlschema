"""Provides the main API and entrypoint to use `xlschema` as a library."""
import logging
from pathlib import Path
import shutil

from . import config
from . import readers
from . import writers as _  # noqa DO NOT DELETE import required for writer registration
from .common.dict import easy_options
from .uri import URIParser

# ----------------------------------------------------------
# Core Application
# ----------------------------------------------------------
__version__ = '0.3.15'


class XLSchemaError(Exception):
    """Cannot convert URI into Schema."""


class XLSchema:
    """Converts specially structured xlfiles to a variety of sql-oriented formats.

    It enables round-trip conversion for rapid data modelling and application
    design. A number of languages are supported and the code has been designed
    to allow easy extension.

    This class is the core application and entrypoint.
    """

    def __init__(self, uri, options=None, **kwds):
        """Main API entrypoint.

        :param uri: uri or path
        :type uri: str

        :param options: argparse options
        :type options: :py:class:`argparse.Namespace`
        """
        self.uri = uri
        self.options = easy_options(options, kwds)
        self.config = config.Config()
        if not self.options.output:
            self.setup_local_dirs()
            self.options.output = self.config.LOCAL_OUTPUT

        self.log = logging.getLogger(self.__class__.__name__)
        self.log.warning('options: %s', self.options)

        # init reader
        self.reader = self.get_reader(self.uri, self.options)
        self.schema = self.reader.schema
        self._writers = []

    def setup_local_dirs(self):
        """Check for and create local directory for data or output files."""
        local_dir = Path(self.config.LOCAL_DIR)
        pkg_root = Path(__file__).absolute().parent
        if not local_dir.exists():
            local_dir.mkdir()
            for directory in ['data', 'templates']:
                source = pkg_root / 'resources' / directory
                target = local_dir / directory
                shutil.copytree(str(source), str(target))

    def _dispatch(self, command, writer_types):
        """Internal method to dispatch arbitrary operations to writer(s).

        :param writer_types: list of writer ids of the form '<file_suffix>/<method>'
        :type writer_types: tuple[str]
        """
        if not writer_types:
            writer_types = self.writer_types

        for writer_type in writer_types:
            writer = self.get_writer(writer_type)
            if not writer:
                continue
            if hasattr(writer, command):
                getattr(writer, command)()
            else:
                self.log.error("Writer '%s' does not have method '%s'",
                               writer_type, command)  # pragma: no cover

    def get_reader(self, uri, options=None, **kwds):
        """Returns a specialized schema reader based parsed uri.

        :param uri: uri or path
        :type uri: str

        :param options: argparse options
        :type options: dict-like object

        :param kwds: override default options or set new options
        :type kwds: dict

        :rtype: :py:class:`xlschema.readers.abstract.SchemaReader`

        Accepts the following file types::

            *.xlsx   -> ExcelToModel(uri, options)
            *.yaml   -> YamlToModel(uri, options)
            <db_uri> -> DBToModel(uri, options)
        """
        options = easy_options(options, kwds)
        self.log.debug('reading %s', uri)

        parsed_uri = URIParser(uri)

        if parsed_uri.type == 'xlsx':
            return readers.ExcelToModel(uri, options)

        elif parsed_uri.type == 'yaml':
            return readers.YamlToModel(uri, options)

        elif parsed_uri.type == 'database':
            if options.sql:
                return readers.SqlToModel(uri, options)
            return readers.DBToModel(uri, options)
        else:
            raise XLSchemaError("'%s' not a valid resource.", uri)

    @property
    def writer_types(self):
        """Returns a list of writer types."""
        return sorted(self.config.WRITERS)

    @property
    def writers(self):
        """Returns a cached list of configured writer instances."""
        if not self._writers:
            self._writers = [self.config.WRITERS[wt](self.schema, self.options)
                             for wt in self.writer_types]
        return self._writers

    def get_writer(self, writer_type):
        """Get a special writer based on type.

        :param writer_type: writer format
        :type writer_type: str

        :rtype: :py:class:`xlschema.writers.abstract.SchemaWriter`
        """
        if writer_type not in self.config.WRITERS:
            self.log.error("Writer '%s' not found.",
                           writer_type)  # pragma: no cover
        else:
            return self.config.WRITERS[writer_type](self.schema, self.options)

    def write(self, *writer_types, to_path=None):
        """Execute write operation of writer(s)."""
        if not writer_types:
            writer_types = self.writer_types

        for writer_type in writer_types:
            writer = self.get_writer(writer_type)
            if not writer:
                continue
            try:
                writer.write(to_path=to_path)
            except KeyError:
                self.log.warning("skipping: %s", writer_type)

    def run(self, *writer_types):
        """Run all default operations of writer(s)."""
        self._dispatch('run', writer_types)

    def populate(self, *writer_types):
        """Execute populate operation of writer(s)."""
        self._dispatch('populate', writer_types)
