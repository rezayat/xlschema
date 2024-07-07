"""Abstract plugin."""
import abc
import logging
# from typing import List

import yaml

from ..common.mixins import CommandMixin


class Plugin(abc.ABC, CommandMixin):
    """Abstract plugin class."""

    name = 'plugin'  # override me
    subcommand = 'plugin'  # override me
    requires = []  # type: List[str]
    is_active = False

    def __init__(self, app, options=None):
        """Plugin constructor.

        :param app: instance of main application
        :param type: :py:class:`xlschema.XLSchema`
        """
        self.app = app
        self.options = options
        self.store = {}
        self.log = logging.getLogger(self.__class__.__name__)
        self.log.debug('loading %s plugin', self.name)

    @staticmethod
    def register_plugin_subparser(app, cls):
        """Helper staticmethod to register subparser and return options."""
        with open(app.config_yml) as cfg:
            yml = yaml.load(stream=cfg, Loader=yaml.SafeLoader)
            plugin_options = yml['settings']['plugins'][cls.subcommand]['options']
            # print(cls.subcommand, 'plugin_options:', plugin_options)
        parser = app.subparsers.add_parser(
            cls.subcommand,
            nspace=plugin_options,
            help=cls.__doc__)
        return parser.add_argument

    @classmethod
    def setup(cls, app, options):
        """Set up and register the plugin class with application."""
        app.plugins[cls.name] = cls(app, options)

    @abc.abstractclassmethod
    def setup_cmdline(cls, app):  # noqa
        """Set up and register cmdline options for the plugin instance."""
        # parser = app.subparsers.add_parser(cls.subcommand, help=cls.__doc__)
        # option = parser.add_argument
        #
        # OR (if parser is not needed)
        #
        # option = self.register_plugin_subparser(cls, app)

    @abc.abstractmethod
    def execute(self, *args, **kwds):
        """Main execution method (must override)."""
