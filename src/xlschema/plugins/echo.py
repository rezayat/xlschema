"""A minimal echo plugin for demo and testing purposes."""
from .abstract import Plugin


class EchoPlugin(Plugin):
    """Echo command-line options."""

    name = 'echo'
    subcommand = 'echo'
    is_active = True

    @classmethod
    def setup_cmdline(cls, app):
        """Set up and register cmdline options for echo plugin instance."""
        option = cls.register_plugin_subparser(app, cls)
        option('--hello', type=str, default='bye', help='prints hello')
        option('foo', help='foo var')

    def execute(self, *args, **kwds):
        """Do nothing except echo command-line options."""
        self.log.debug('options: %s', self.options)
        self.store['success'] = True
