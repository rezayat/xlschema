"""Contains uri handling logic for xlschema."""
import logging
from pathlib import Path

import sqlalchemy
from sqlalchemy.engine.url import make_url

from .common import utils


class URIParser:
    """Determines whether a uri is a xlsx/yaml file or a db_uri."""

    def __init__(self, uri: str) -> None:
        """Class constructor.

        :param uri: Uniform resource identifier.
        :type uri: str
        """
        self.uri = uri
        self.type = None  # xlsx|yaml|database

        # if type == db
        self.db_uri = None  # parsed uri
        self.db_type = None

        self.log = logging.getLogger(self.__class__.__name__)
        self.parse()

    def parse(self):
        """Parse uri and set self.type to appropriate value."""
        try:
            # assume it is a db_uri
            self.db_uri = make_url(self.uri)
            self.type = 'database'
            self.db_type = self.db_uri.drivername
        except sqlalchemy.exc.ArgumentError:
            # assume it is a file
            if self.is_xlsx:
                self.type = 'xlsx'
            if self.is_yaml:
                self.type = 'yaml'

    @property
    def name(self) -> str:
        """Return parsed name of uri."""
        _name = None
        if self.type in ['xlsx', 'yaml']:
            _name = Path(self.uri).stem
        if self.type == 'database':
            if self.db_type == 'sqlite':
                _name = Path(self.db_uri.database).stem
            else:
                _name = self.db_uri.database
        return _name

    @property
    def is_xlsx(self) -> bool:
        """Returns true if uri is a ``*.xlsx`` file."""
        return utils.is_xlsx(self.uri)

    @property
    def is_yaml(self) -> bool:
        """Returns true if uri is a ``*.yaml`` or ``*.yml`` file."""
        return utils.is_yaml(self.uri)

    @property
    def is_db_uri(self) -> bool:
        """Returns true if uri is a valid db_uri."""
        return bool(self.db_uri)
