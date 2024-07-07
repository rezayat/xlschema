"""Field classes for JVM languages.

Inheritance structure::

    Field
        JavaField
        ScalaField

"""

from . import constants
from ..common import utils
from .abstract import Field


class JavaField(Field):
    """Java specialized field type."""

    TYPES = utils.dictmerge(
        constants.TYPES_COMMON,
        interval='Duration'
    )

    @property
    def definition(self):
        """Define java bean columns."""
        # change name
        args = []
        typeclass = self.TYPES[self._type]
        fieldname = self.name
        camelcase = fieldname.under_to_mixed()

        if self.is_pk:
            args.append('@Id')
            args.append('@GeneratedValue(strategy = GenerationType.IDENTITY)')
        else:
            if self.is_fk:
                args.append('@ManyToOne(cascade = CascadeType.ALL)')
                args.append('@JoinColumn(name = "{}")'.format(fieldname))
            else:
                args.append('@Column(name="{}")'.format(fieldname))

        args.append('private {} {};'.format(typeclass, camelcase))
        args.append('\n')
        return "\n    ".join(args)

    @property
    def method(self):
        """Define java bean method."""
        # change name
        args = []
        fieldname = self.name
        camelcase = fieldname.under_to_mixed()
        classname = fieldname.classname

        args.append('public {} get{}() {{'.format(self.type, classname))
        args.append('    return this.{};'.format(camelcase))
        args.append('}')
        args.append('\n')
        args.append('public void set{}({} {}) {{'.format(
            classname, self.type, fieldname))
        args.append('    this.{} = {};'.format(camelcase, fieldname))
        args.append('}')

        args.append('\n')
        return "\n    ".join(args)


class ScalaField(JavaField):
    """Java specialized field type."""

    @property
    def definition(self):
        """Define java bean columns."""
        # change name
        args = []
        typeclass = self.TYPES[self._type]
        fieldname = self.name
        camelcase = fieldname.under_to_mixed()

        if self.is_pk:
            args.append('@Id')
            args.append('@GeneratedValue(strategy = GenerationType.IDENTITY)')
            args.append('@BeanProperty')
            args.append('var {}: {} = _'.format(fieldname, typeclass))
        else:
            if self.is_fk:
                args.append('@ManyToOne(cascade = CascadeType.ALL)')
                args.append('@JoinColumn(name = "{}")'.format(fieldname))
                args.append('var {}: {} = {}'.format(
                    camelcase, typeclass, fieldname))
            else:
                args.append('@BeanProperty')
                args.append('var {}: {} = {}'.format(
                    camelcase, typeclass, fieldname))

        args.append('\n')
        return "\n    ".join(args)
