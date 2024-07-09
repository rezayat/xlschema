"""Sheet classes used by xlsx readers.

Sheet types are used by readers to differentiate sheet specs from
one another.
"""
import logging
from collections import OrderedDict
# from typing import List

from ... import fields, models
from ...common.list import List as ListUtils
from ...config import Config

# ----------------------------------------------------------------------
# XL Sheet Types
# ----------------------------------------------------------------------


class XlSheet(object):
    """Abstract base excel sheet type."""

    FORMAT = ''

    def __init__(self, xlsheet, options=None):
        """Sheet initializer.

        :param xlsheet: parsed sheet of excel workbook
        :param type: :py:class:`openpyxl.worksheet.worksheet.Worksheet`
        """
        self.name = xlsheet.title
        self.xlsheet = xlsheet
        self.options = options
        self.log = logging.getLogger(self.__class__.__name__)
        self.config = Config()

    def __repr__(self):
        return "<{} '{}'>".format(self.__class__.__name__, self.name)

    def parse(self):
        """Parse excel sheet data."""

    def write(self):
        """Write to an excel sheet."""

    def generate(self):
        """Generate an empty excel sheet without data."""


class EnumSheet(XlSheet):
    """Enum sheet type."""

    def __init__(self, xlsheet, options=None):
        """Class constructor.

        :param xlsheet: parsed sheet of excel workbook
        :param type: :py:class:`openpyxl.worksheet.worksheet.Worksheet`
        """
        super(EnumSheet, self).__init__(xlsheet, options)
        self.enums = {}

    def parse(self):
        """Processes ENUMs sheet in the xlfile."""
        self.log.debug('parsing: %s', self.name)
        # print('xlsheet.rows:', list(self.xlsheet.rows))
        rows = []
        for row in self.xlsheet.rows:
            try:
                row = row[0], row[1]  # just in case rows are longer than 2
                row = tuple([i.value for i in row])
                rows.append(row)
                self.log.debug('reading enum: %s', row)
            except IndexError:
                self.log.error('skipping: ENUMs sheet empty')
                return

        for enum in ListUtils.isplit(rows, (None, None)):
            head, tail = enum[0], enum[1:]
            _enum = models.Enum(
                name=head[0], data=[(key, val) for (key, val) in tail])
            self.enums[_enum.name] = _enum
        self.log.debug('enums: %s', self.enums)


class ModelSheet(XlSheet):
    """Abstract model base sheet type."""

    PROPERTIES = []  # type: List[str]
    METAFIELDS = Config.METAFIELDS
    field_class = fields.Field
    model_class = models.Model

    def __init__(self, xlsheet, options=None):
        """Class constructor.

        :param xlsheet: parsed sheet of excel workbook
        :param type: :py:class:`openpyxl.worksheet.worksheet.Worksheet`
        """
        super(ModelSheet, self).__init__(xlsheet, options)
        self.model = None
        self.data = None

    @property
    def n_properties(self):
        """Returns the number of properties for the sheet class."""
        return len(self.PROPERTIES)

    @property
    def n_metafields(self):
        """Returns the number of metafields for the sheet class."""
        return len(self.METAFIELDS)


class DataSheet(ModelSheet):
    """A basic sheet with data."""

    FORMAT = 'left-data'

    def _parse_metadata(self, rows):
        """Returns zip of metadata."""
        def _parse_row(row):
            """Returns value of each cell in row (skipping first)."""
            return [cell.value for cell in row][1:]

        return list(
            zip(*[_parse_row(rows[i]) for i in range(self.n_metafields)]))

    def _parse_metafield_data(self, offset=0):
        """Returns returns list of metafield data."""
        self.log.debug('\tparsing %s metadata', self.name)
        # field metadata values are in reverse and must be flipped around
        return [
            list(reversed(list(args)))
            for args in self._parse_metadata(list(self.xlsheet.rows)[offset:])
        ]

    def _parse_data(self, offset=0):
        """Returns row by row data."""
        self.log.debug('\tparsing %s data', self.name)
        data = list(self.xlsheet.rows)[self.n_metafields + offset:]
        row_values = []
        for row in ListUtils.iterate(data):
            row = row[1:]
            if not row[0].value:  # to skip empty rows
                continue
            row_values.append([c.value for c in row])
        return row_values

    def parse(self):
        """Processes an xlsheet with embedded data."""
        self.log.debug('parsing: %s', self.name)

        # metafields
        metafield_data = self._parse_metafield_data()

        # fields
        _fields = [self.field_class(*args) for args in metafield_data]

        # data
        data = self._parse_data()

        # populate model
        self.model = models.Model(self.name, _fields, data)


class NoDataSheet(ModelSheet):
    """A basic sheet without data."""

    FORMAT = 'no-data'

    def _parse_fields(self):
        """Returns list of fields."""
        self.log.debug('\tparsing %s metadata', self.name)
        _fields = []
        for row in list(self.xlsheet.rows)[2:]:
            args = tuple([i.value for i in row])
            self.log.debug('reading: %s', args)
            _fields.append(self.field_class(*args))
        return _fields

    def parse(self):
        """Processes an xlsheet without embedded data."""
        self.log.debug('parsing: %s', self.name)

        # metadata
        _fields = self._parse_fields()

        # populate model
        self.model = models.Model(self.name, _fields)


class PropertySheet(DataSheet):
    """A sheet for apps, packages or anything that needs properties."""

    FORMAT = 'property'
    PROPERTIES = [
        'app',
        'model',
    ]

    def _parse_properties(self):
        """Parse properties at top of sheet.

        Properties by be separated from the metadata section
        by a blank row
        """
        self.log.debug('\tparsing %s properties', self.name)
        items = []
        for row in self.xlsheet.rows:
            if row[0].value and row[1].value:
                items.append((row[0].value, row[1].value))
            else:
                break
        return OrderedDict(items)

    def parse(self):
        """Processes an xlsheet with embedded data."""
        self.log.debug('parsing: %s', self.name)
        offset = self.n_properties + 1

        # properties
        properties = self._parse_properties()

        # metafields
        metafield_data = self._parse_metafield_data(offset)

        # fields
        _fields = [self.field_class(*args) for args in metafield_data]

        # data
        data = self._parse_data(offset)

        # populate model
        self.model = models.Model(self.name, _fields, data, properties)
