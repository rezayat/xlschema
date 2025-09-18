"""Core XLSchema plugin."""
import argparse
import os

from .. import XLSchema
from ..common.context_managers import Timer
from ..config import Config
from .abstract import Plugin


class CorePlugin(Plugin):
    """Generate model code from URI."""

    name = 'core'
    subcommand = 'from_uri'
    is_active = True

    FORMATS = ', '.join(sorted(Config.WRITERS.keys()))

    @classmethod
    def setup_cmdline(cls, app):
        """Set up and register cmdline options for core plugin instance."""
        option = cls.register_plugin_subparser(app, cls)
        # bool options
        option('--run', '-r', action='store_true', help='autorun with all options')
        option('--populate', '-p', action='store_true', help='populate database')
        option('--update-only', '-u', action='store_true', help='only gen update code')
        option('--models-only', action='store_true', help='only gen model code')
        option('--view', '-v', action='store_true', help='include views')

        # sql options
        option('--table', '-t', nargs='*', help="table(s) to dump")
        option('--sql', '-s', nargs='*', help='sql to use for selection')

        # multi-string options with basic validation
        def validate_single_format(value):
            from ..common.validation import validate_format_string, ValidationError
            try:
                # Only do basic pattern validation, not strict format checking for backward compatibility
                return validate_format_string(value, allowed_formats=None)
            except ValidationError as e:
                # For backward compatibility, log warning but don't fail
                import logging
                logging.getLogger('xlschema.plugins.core').warning(f"Format validation warning: {e}")
                return value

        option('--format', '-f', type=validate_single_format, nargs='*', help=cls.FORMATS)

        # required
        option('uri', help="uri to operate on")

    def execute(self, *args, **kwds):
        """Converts uri, a file or db_uri, to multiple formats."""
        with Timer(self.log):

            xlschema = XLSchema(self.options.uri, self.options)
            if self.options.output:
                if not os.path.exists(self.options.output):
                    os.makedirs(self.options.output)

            if self.options.format:

                if self.options.run:
                    for fmt in self.options.format:
                        self.log.info('running to %s using %s method',
                                      self.options.output, fmt)
                        xlschema.run(fmt)

                else:
                    for fmt in self.options.format:
                        self.log.info('writing to %s using %s method',
                                      self.options.output, fmt)
                        xlschema.write(fmt)

                    if self.options.populate:
                        self.log.warning('populating options triggered')
                        xlschema.populate(self.options.format)

            elif self.options.run:
                self.log.info('running all methods to %s', self.options.output)
                xlschema.run()

            else:
                self.log.info('writing all methods to %s', self.options.output)
                xlschema.write()

        self.store['success'] = True
