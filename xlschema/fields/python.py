"""Field classes for the python language and its frameworks.

Inheritance structure::

    Field
        SqlAlchemyField
        DjangoField
        FactoryBoyField
"""

from . import constants
from ..common import utils
from ..common.text import Text
from .abstract import Field


class SqlAlchemyField(Field):
    """Sqlalchemy specialized field type."""

    TYPES = utils.dictmerge(
        constants.TYPES_COMMON,
        interval='Interval'
    )

    @property
    def definition(self):
        """Sqlalchemy model column definition."""
        relationship = None
        typeclass = self.TYPES[self._type]
        args = []
        fieldname = Text(self.name.strip_id())

        def fk_args():
            """Internal function to set fkey logic."""
            _fk_args = ['"{}.id"'.format(fieldname)]
            if 'on delete cascade' in self.constraint:
                _fk_args.append("ondelete='CASCADE'")
            if 'on update cascade' in self.constraint:
                _fk_args.append("onupdate='CASCADE'")
            return ', '.join(_fk_args)

        if self.is_pk:
                # primary key is always not null and not blank
            args.append('nullable=False')
            args.append('primary_key=True')
        elif self.is_fk:
            args.append('ForeignKey({})'.format(fk_args()))
            args.append('nullable={}'.format(not self.required))
            relationship = '{} = relationship("{}", backref="{}")'.format(
                fieldname, fieldname.classname, self.model.name.plural())
            relationship = Text(relationship).indent()
        elif self.is_pfk:
            args.append('ForeignKey({})'.format(fk_args()))
            args.append('nullable=False')
            args.append('primary_key=True')
            relationship = '{} = relationship("{}", backref="{}")'.format(
                fieldname, fieldname.classname, self.model.name.plural())
            relationship = Text(relationship).indent()
        else:
            args.append('nullable={}'.format(not self.required))
            if self.is_enum:
                typeclass = self.name.upper()
                # args.insert(0, self.name.upper())
            if self.default:
                args.append('default="{}"'.format(self.default))
            if self.description:
                args.append('doc="{}"'.format(self.description))

        # other settings
        if self.length and self._type == 'str':
            typeclass = 'String({})'.format(self.length)
            # args.insert(0, 'String({})'.format(self.length))

        _definition = "{} = Column({}, {})".format(
            self.name, typeclass, ', '.join(args))
        if relationship:
            _definition = '\n'.join([_definition, relationship])
        return _definition


class DjangoField(Field):
    """Django specialized field type."""

    TYPES = {
        'int': 'IntegerField',
        'serial': 'IntegerField',
        'dec': 'FloatField',
        'float': 'FloatField',
        'double': 'FloatField',
        'txt': 'TextField',
        'str': 'CharField',
        'bool': 'BooleanField',
        'date': 'DateField',
        'time': 'TimeField',
        'interval': 'DurationField',
    }

    @property
    def definition(self):
        """Define django model columns."""
        args = []
        typeclass = self.TYPES[self._type]
        fieldname = self.name

        if self.is_pk:
            # primary key is always not null and not blank
            args.append('blank=False')
            args.append('null=False')
            args.append('primary_key=True')
        else:
            args.append('blank={}'.format(not self.required))
            args.append('null={}'.format(not self.required))

            if self.is_fk:
                fieldname = fieldname.strip_id()
                typeclass = 'ForeignKey'
                if self.is_self_referential:
                    _refers_to = 'self'
                    args.append('related_name="children"')
                else:
                    _refers_to = self.name.classname[:-2]
                args.insert(0, '"{}"'.format(_refers_to))
                args.append('on_delete=models.CASCADE')
            else:
                if self.is_enum:
                    args.append('choices={}'.format(self.name.upper()))
                if self.default:
                    args.append('default="{}"'.format(self.default))
                if self.description:
                    args.append('help_text="{}"'.format(self.description))

        # other settings
        if self._type == 'str':
            if self.length:
                args.append('max_length={}'.format(self.length))
            else:
                typeclass = self.TYPES['txt']

        return "{} = models.{}({})".format(fieldname, typeclass, ', '.join(args))


class FactoryBoyField(Field):
    """Factory Boy fields.

    factory_boy is a fixtures replacement which aims to replace static,
    hard to maintain fixtures with easy-to-use factories for complex object.

    Instead of building an exhaustive test setup with every possible
    combination of corner cases, factory_boy allows you to use objects
    customized for the current test, while only declaring the test-specific
    fields.

    See: https://github.com/FactoryBoy/factory_boy
    """

    TYPES = {
        'int': 'pyint',
        'serial': 'pyint',
        'dec': 'pyfloat',
        'float': 'pyfloat',
        'double': 'pyfloat',
        'txt': 'text',
        'str': 'pystr',
        'bool': 'pybool',
        'date': 'date',
        'time': 'time',
        'interval': 'time_delta',
    }

    # maps names to faker providers
    FAKER_PROVIDERS = {
        # name : provider
        'address': 'address',
        'am_pm': 'am_pm',
        'binary': 'binary',
        'boolean': 'boolean',
        'bothify': 'bothify',
        'bs': 'bs',
        'building_number': 'building_number',
        'catch_phrase': 'catch_phrase',
        'century': 'century',
        # 'chrome': 'chrome',
        'city': 'city',
        'location': 'city',
        'city_prefix': 'city_prefix',
        'city_suffix': 'city_suffix',
        'color': 'color_name',
        'company': 'company',
        'company_email': 'company_email',
        'company_suffix': 'company_suffix',
        'country': 'country',
        'country_code': 'country_code',
        'credit_card_expire': 'credit_card_expire',
        'credit_card_full': 'credit_card_full',
        'credit_card_number': 'credit_card_number',
        'credit_card_provider': 'credit_card_provider',
        'credit_card_security_code': 'credit_card_security_code',
        'cryptocurrency_code': 'cryptocurrency_code',
        'currency_code': 'currency_code',
        'date': 'date',
        'date_object': 'date_object',
        'date_time': 'date_time',
        'date_time_ad': 'date_time_ad',
        'date_time_between': 'date_time_between',
        'date_time_between_dates': 'date_time_between_dates',
        'date_time_this_century': 'date_time_this_century',
        'date_time_this_decade': 'date_time_this_decade',
        'date_time_this_month': 'date_time_this_month',
        'date_time_this_year': 'date_time_this_year',
        'day_of_month': 'day_of_month',
        'day_of_week': 'day_of_week',
        'domain_name': 'domain_name',
        'domain_word': 'domain_word',
        'ean': 'ean',
        'ean13': 'ean13',
        'ean8': 'ean8',
        'email': 'email',
        'file_extension': 'file_extension',
        'file_name': 'file_name',
        'file_path': 'file_path',
        # 'firefox': 'firefox',
        'first_name': 'first_name',
        'first_name_female': 'first_name_female',
        'first_name_male': 'first_name_male',
        # 'format': 'format',
        'free_email': 'free_email',
        'free_email_domain': 'free_email_domain',
        'future_date': 'future_date',
        'future_datetime': 'future_datetime',
        'geo_coordinate': 'geo_coordinate',
        # 'get_formatter': 'get_formatter',
        # 'get_providers': 'get_providers',
        'hex_color': 'hex_color',
        'image_url': 'image_url',
        # 'internet_explorer': 'internet_explorer',
        'ipv4': 'ipv4',
        'ipv6': 'ipv6',
        'isbn10': 'isbn10',
        'isbn13': 'isbn13',
        'iso8601': 'iso8601',
        'job': 'job',
        'language_code': 'language_code',
        'last_name': 'last_name',
        'last_name_female': 'last_name_female',
        'last_name_male': 'last_name_male',
        'latitude': 'latitude',
        'lexify': 'lexify',
        'license_plate': 'license_plate',
        'linux_platform_token': 'linux_platform_token',
        'linux_processor': 'linux_processor',
        'locale': 'locale',
        'longitude': 'longitude',
        'mac_address': 'mac_address',
        'mac_platform_token': 'mac_platform_token',
        'mac_processor': 'mac_processor',
        'md5': 'md5',
        # 'military_apo': 'military_apo',
        # 'military_dpo': 'military_dpo',
        # 'military_ship': 'military_ship',
        # 'military_state': 'military_state',
        'mime_type': 'mime_type',
        'month': 'month',
        'month_name': 'month_name',
        'name': 'name',
        'name_female': 'name_female',
        'name_male': 'name_male',
        'null_boolean': 'null_boolean',
        'numerify': 'numerify',
        # 'opera': 'opera',
        'paragraph': 'paragraph',
        'paragraphs': 'paragraphs',
        # 'parse': 'parse',
        'password': 'password',
        'past_date': 'past_date',
        'past_datetime': 'past_datetime',
        'phone_number': 'phone_number',
        'postalcode': 'postalcode',
        'postalcode_plus4': 'postalcode_plus4',
        'postcode': 'postcode',
        'prefix': 'prefix',
        'prefix_female': 'prefix_female',
        'prefix_male': 'prefix_male',
        # 'profile': 'profile',
        # 'provider': 'provider',
        # 'providers': 'providers',
        # 'pybool': 'pybool',
        # 'pydecimal': 'pydecimal',
        # 'pydict': 'pydict',
        # 'pyfloat': 'pyfloat',
        # 'pyint': 'pyint',
        # 'pyiterable': 'pyiterable',
        # 'pylist': 'pylist',
        # 'pyset': 'pyset',
        # 'pystr': 'pystr',
        # 'pystruct': 'pystruct',
        # 'pytuple': 'pytuple',
        # 'random': 'random',
        'random_digit': 'random_digit',
        'random_digit_not_null': 'random_digit_not_null',
        'random_digit_not_null_or_empty': 'random_digit_not_null_or_empty',
        'random_digit_or_empty': 'random_digit_or_empty',
        'random_element': 'random_element',
        'random_int': 'random_int',
        'random_letter': 'random_letter',
        'random_number': 'random_number',
        'random_sample': 'random_sample',
        'random_sample_unique': 'random_sample_unique',
        'randomize_nb_elements': 'randomize_nb_elements',
        'rgb_color': 'rgb_color',
        'rgb_css_color': 'rgb_css_color',
        # 'safari': 'safari',
        'safe_color_name': 'safe_color_name',
        'safe_email': 'safe_email',
        'safe_hex_color': 'safe_hex_color',
        'secondary_address': 'secondary_address',
        # 'seed': 'seed',
        # 'seed_instance': 'seed_instance',
        'sentence': 'sentence',
        'sentences': 'sentences',
        # 'set_formatter': 'set_formatter',
        'sha1': 'sha1',
        'sha256': 'sha256',
        # 'simple_profile': 'simple_profile',
        'slug': 'slug',
        'ssn': 'ssn',
        'state': 'state',
        'state_abbr': 'state_abbr',
        'street_address': 'street_address',
        'street_name': 'street_name',
        'street_suffix': 'street_suffix',
        'suffix': 'suffix',
        'suffix_female': 'suffix_female',
        'suffix_male': 'suffix_male',
        'text': 'text',
        'time': 'time',
        'time_delta': 'time_delta',
        'time_object': 'time_object',
        'time_series': 'time_series',
        'timezone': 'timezone',
        'tld': 'tld',
        'unix_time': 'unix_time',
        'uri': 'uri',
        'uri_extension': 'uri_extension',
        'uri_page': 'uri_page',
        'uri_path': 'uri_path',
        'url': 'url',
        'user_agent': 'user_agent',
        'user_name': 'user_name',
        'uuid4': 'uuid4',
        # 'windows_platform_token': 'windows_platform_token',
        'word': 'word',
        # 'words': 'words',
        'year': 'year',
        'zipcode': 'zipcode',
        'zipcode_plus4': 'zipcode_plus4',
    }

    @property
    def definition(self):
        """Defines a factory per field."""
        provider = self.TYPES[self._type]
        fakertype = "factory.Faker('{}')"
        name = self.name

        if self.is_pk and self._type in ['int', 'serial']:
            fakertype = "factory.Sequence(lambda n: n)"

        elif self.is_fk:
            name = self.name.strip_id()
            if name in ['parent'] and self.model.has_app_model_properties:
                classname = '{}.factories.{}'.format(
                    self.model.properties['app'],
                    self.model.name.classname)
                fakertype = "factory.SubFactory('{}Factory')".format(classname)
            else:
                classname = Text(name).classname
                fakertype = "factory.SubFactory({}Factory)".format(classname)
        else:
            if name in self.FAKER_PROVIDERS:
                provider = self.FAKER_PROVIDERS[name]
            fakertype = "factory.Faker('{}')".format(provider)

            if self.is_enum:
                fakertype = 'factory.Iterator(model.{})'.format(name.upper())

        return "{} = {}".format(name, fakertype)
