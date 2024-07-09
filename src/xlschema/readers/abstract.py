"""Abstract Transformer Classes."""

import abc
import logging
from typing import List

from ..config import Config
from ..fields import Field
from ..models import Schema
from ..uri import URIParser


class SchemaReader(abc.ABC):
    """Abstract base class for schema-based readers.

    Parses uris (.xlsx, .yaml) into relational models.

    Can parse three formats:
        1. Schema without data

        2. Schema with data
            a. without left header: data from A1
            b. with left header: data from B1

        3. Schemas with properties and data

    In each case each sheet corresponds to one model
    with a required 'ENUMs' sheet to designate enumerations.

    At the end of each successful parsing run:
        - ``.models`` must be populated with :py:class:`xlschema.models.Model` instances
        - ``.enums`` must be populated with :py:class:`xlschema.models.Enum` instances
        - ``.types`` must be populated with a set of types used in the schema
    """

    def __init__(self, uri: str, options: dict = None) -> None:
        """Init SchemaReader.

        :param uri: a file or db_uri
        :param options: optional dict-like namespace
        """
        self.uri = uri
        self.parsed_uri = URIParser(uri)
        self.schema = Schema(name=self.parsed_uri.name)
        self.field_class = Field
        self.options = options
        self.config = Config()
        self.log = logging.getLogger(self.__class__.__name__)
        # run main methods automatically
        self.preprocess()
        self.process()

    @abc.abstractmethod
    def preprocess(self):
        """Runs before main process for conversion."""

    @abc.abstractmethod
    def process(self):
        """Main process for conversion."""

    def post_process(self, model_names: List[str]) -> None:
        """Creates a set of all types used in the schema.

        This is useful for deciding on imports in code generation use
        cases.
        """
        mtm_tables = self.identify_mtm_tables(model_names)
        for model in self.schema.models:
            self.log.debug('post-processing: %s', model.name)
            if model.name in mtm_tables:
                model.metadata['is_mtm'] = True
            for field in model.fields:
                self.schema.types.add(field.type)

    @staticmethod
    def identify_mtm_tables(model_names: List[str]) -> List[str]:
        """Identifies many to many tables.

        Tables are identified from their name pattern of a middle underscore
        and the existence of the referenced tables in the schema.
        """
        _mtm_tables = []
        for name in model_names:
            if '_' in name:
                words = name.split('_')
                if len(words) % 2 == 0:  # length of words is even
                    mid = len(words) // 2
                    table1, table2 = '_'.join(words[mid:]), '_'.join(
                        words[:mid])
                    if (table1 in model_names) and (table2 in model_names):
                        _mtm_tables.append(name)
        return _mtm_tables
