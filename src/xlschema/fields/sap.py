"""Field classes for SAP languages.

Inheritance structure::

    Field
        AbapField
"""

from .sql import SqlField


class AbapField(SqlField):
    """Field type to be used in SAP Abap code generation."""

    TYPES = {
        'str': 'STRING',     # specified size text
        'txt': 'STRING',     # arbitrary size text
        'date': 'D',         # date
        'time': 'T',         # time
        'interval': 'T',     # interval (not checked)
        'bool': 'C',         # bool
        'int': 'I',          # int4
        'dec': 'F',          # single precision floating point
        'float': 'F',        # single precision floating point
        'double': 'F',       # double precision floating point
        'numeric': 'F',      # double precision floating point
        'serial': 'serial',  # auto pk (int)
    }

    @property
    def comma(self):
        """Comma prop for adding comma at end of line."""
        if self.is_last:
            return '.'
        return ','

    @property
    def default(self):
        """ABAP specific default value."""
        if self._default:
            if isinstance(self._default, str):
                _default = "'{}'".format(self._default)
            else:
                _default = "{}".format(self._default)

            return "VALUE {}".format(_default)

    @property
    def definition(self):
        """ABAP column definition."""
        _def = "{:<10} {}".format(self.name, self.type)
        if self.default:
            _def = "{:<10} {} {}".format(
                self.name, self.type, self.default)
        # glue def and other parts together
        _def += self.comma
        return '{:<30} " {}'.format(_def, self.description)
