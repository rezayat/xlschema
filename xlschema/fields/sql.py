"""Field classes for SQL dialects.

Inheritance structure::

    Field
        SqlField
            PostgresField
                PgEnumField
            SqliteField
"""

import re

from .abstract import Field


class SqlField(Field):
    """Field type to be used in sql code generation."""

    TYPES = {
        'str': 'varchar({})',    # specified size text
        'txt': 'text',           # arbitrary size text
        'date': 'date',          # date
        'time': 'time',          # time without date
        'interval': 'interval',  # interval between timestamps
        'bool': 'boolean',       # binary
        'int': 'integer',        # int4
        'dec': 'float',          # single precision floating point
        'float': 'float',        # single precision floating point
        'double': 'double',      # double precision floating point
        'numeric': 'numeric',    # double precision floating point
        'serial': 'serial',      # auto pk (int)
    }

    CONSTRAINT_PATTERNS = {
        'check': re.compile(r'^check\s*\(.+\)'),
        'unique': re.compile('^unique'),
        'on update|delete cascade': re.compile(
            r'^(on\s(delete|update)\scascade)'
            r'(\son\s(delete|update)\scascade)?'),
    }

    @property
    def required_qualifier(self):
        """Keyword in sql to signify not null."""
        return 'not null'

    @property
    def is_valid_constraint(self):
        """Check using regex if constraint fits specific patterns."""
        for pattern in self.CONSTRAINT_PATTERNS:
            if self.CONSTRAINT_PATTERNS[pattern].match(self.constraint.lower()):
                return True
        return False

    @property
    def default(self):
        """A sql-specific default value."""
        if self._default in [0, 0.0] or self._default:
            if isinstance(self._default, str):
                _default = "'{}'".format(self._default)
            else:
                _default = "{}".format(self._default)

            return "default {}".format(_default)

    @property
    def definition(self):
        """SQL column definition with constraints."""
        args = [self.name, self.type]

        if self.is_pk:
            args += ['primary key']

        elif self.is_fk or self.is_pfk:
            if self.is_self_referential:
                args += ['references', self.model_name, '(id)']
            else:
                args += ['references', self.name.strip_id(), '(id)']

        elif self.default:
            args += [self.default]

        if self.is_valid_constraint:
            args += [self.constraint]

        if self.is_required:
            args += [self.required_qualifier]

        # glue def and other parts together
        _def = ' '.join(args) + self.comma
        if self.offset:
            offset = self.offset - len(_def)
            _comment = "-- {}".rjust(offset).format(self.description)
            result = "{} {}".format(_def, _comment)
        else:
            result = _def
        return result


class PostgresField(SqlField):
    """Postgres specialized field type."""


class PgEnumField(PostgresField):
    """Postgres specialized field type for pgsql with enums."""

    @property
    def type(self):
        """Field type to handle enum special case."""
        _type = self._typecheck()
        if self.is_enum:  # override for enum
            _type = self.name
        return _type


class SqliteField(SqlField):
    """Sqlite specialized field type."""
