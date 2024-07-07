"""A plugin to display information about writer types and classes."""
from ..config import Config
from .abstract import Plugin


class DisplayPlugin(Plugin):
    """Display available writers."""

    name = 'display'
    subcommand = 'display'
    is_active = True

    @classmethod
    def setup_cmdline(cls, app):
        """Set up and register cmdline options for display plugin instance."""
        opt = cls.register_plugin_subparser(app, cls)
        opt('--offset', '-o', type=int, default=20, help='left column offset')
        opt('--qualify', '-q', action='store_true', help='qualify writer class')

    def execute(self, *args, **kwds):
        """Display table of writer types and reader types."""
        self.log.debug('options: %s', self.options)
        offset = self.options.offset
        writer_types = sorted(Config.WRITERS)
        writer_classes = [Config.WRITERS[wt] for wt in writer_types]

        def rst(entry):
            """Conditionally qualify the writer class reference."""
            if self.options.qualify:
                return ':py:class:`xlschema.writers.{}`'.format(entry)
            return entry

        max_len_writer_type = max(len(wt) for wt in writer_types)
        max_len_writer_class = max(
            len(rst(wc.__name__)) for wc in writer_classes)

        def line():
            """Adaptive line with length as max len of elements in columns."""
            return "{0:<{1}}{2}".format(
                '=' * max_len_writer_type,
                offset,
                '=' * max_len_writer_class)
        print()
        print(line())
        print("{0:<{1}}{2}".format('Writer Type', offset, 'Writer Class'))
        print(line())
        for writer_type, writer_class in zip(writer_types, writer_classes):
            print('{0:<{1}}{2}'.format(
                writer_type,
                offset,
                rst(writer_class.__name__)))
        print(line())
        print()
        self.store['success'] = True
