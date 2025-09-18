"""A plugin to integrate sqlacodegen."""
import os

from ..common.text import Text
from ..config import Config
from .abstract import Plugin


class SqlaCodegenPlugin(Plugin):
    """Generate sqlalchemy schemas from databases."""

    name = 'sqlacodegen'
    subcommand = 'to_sqla'
    requires = ['sqlacodegen']
    is_active = True

    @classmethod
    def setup_cmdline(cls, app):
        """Set up and register cmdline options for sqlacodegen plugin instance."""
        option = cls.register_plugin_subparser(app, cls)
        option('--uri', '-u', type=str, help='set db uri', default=Config.DB_URI)
        option('--view', '-v', action='store_true', help='include views')
        option('table', nargs='*', help="table(s) to dump")

    def execute(self, *args, **kwds):
        """Generate sqlalchemy code from db uri."""
        if self.options.table:
            tables = "--tables {}".format(','.join(self.options.table))
        else:
            tables = ''
        if self.options.prefix:
            prefix = self.options.prefix
        else:
            prefix = Text.timestamp()
        outfile = '{}_sqla_schema.py'.format(prefix)
        self.log.debug('generating sqlacodegen schema: %s', outfile)
        _cmd = "sqlacodegen --noviews "
        if tables:
            _cmd += tables
        _cmd += ' --outfile {} {}'.format(
            os.path.join(self.options.output, outfile),
            self.options.uri)
        self.cmd(_cmd, fail_ok=True)

        self.store['success'] = True
