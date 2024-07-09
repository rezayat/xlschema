"""Commandline classes."""
import argparse
import logging
import logging.config
import pathlib
import sys

import yaml

from . import list_plugins
from ..common.mixins import CommandMixin
from ..config import Config
from ..ext.appsettings import SettingsParser


class PluginApplication(CommandMixin):
    """Title: <one line description>."""

    name = 'name'
    description = 'description here'
    epilog = ''
    version = '0.0.1'
    default_args = ['--help']
    config_yml = pathlib.Path(__file__).parent.parent / '.xlschema.yml'

    def __init__(self):
        """Initialize and configure commandline application."""
        self.config = Config()
        self.log = logging.getLogger(self.__class__.__name__)
        self.active_plugin_classes = list_plugins()
        self.plugins = {}
        self.parser = SettingsParser(
            prog=self.name,
            description=self.description,
            epilog=self.epilog,
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
            nspace=self.configure_global_options(),
        )
        self.subparsers = None

    def configure_global_options(self):
        """Loads and returns global options, logging config from .yml file."""
        with open(self.config_yml) as cfg:
            yml = yaml.safe_load(stream=cfg)
        logging.config.dictConfig(yml['logging'])
        global_options = yml['settings']['global']['options']
        return global_options

    def _setup_plugins_cmdline(self):
        """Sets up plugins commandline subparsers."""
        if self.active_plugin_classes:
            self.subparsers = self.parser.add_subparsers(
                dest='plugin', metavar='plugin')
            for plugin_class in self.active_plugin_classes:
                plugin_class.setup_cmdline(self)

    def _setup_plugins(self, options):
        """Sets up all plugin instances and registers with app.plugins dict."""
        for plugin_class in self.active_plugin_classes:
            plugin_class.setup(self, options)

    def _execute_plugins(self, options):
        """Execute all active plugin instances."""
        for name in self.plugins:
            if getattr(options, 'plugin') == self.plugins[name].subcommand:
                self.plugins[name].execute()

    def set_general_options(self):
        """Set general or application-wide options."""
        # option = self.parser.add_argument
        # option('--output', '-o', type=str, help='set output directory')
        # option('--prefix', type=str, help="set prefix of output")
        # option('--clean', '-c', action='store_true', help='clean output dir before generation')

    def cmdline(self):
        """Main method and commandline entrypoint."""
        # add general options
        self.set_general_options()

        # setup plugins commandline sub-commands
        self._setup_plugins_cmdline()

        # capture case with no arguments
        if len(sys.argv) == 1:
            self.parser.print_help()
            sys.exit(1)

        # get options from user
        options = self.parser.parse_args()

        # normalize options
        # options = normalize_options(options, use_objdict=True)
        self.log.debug('options: %s', options)

        # register plugins
        self._setup_plugins(options)

        # execute plugins finally
        self._execute_plugins(options)
