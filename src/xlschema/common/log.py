"""A custom logging class."""

import logging

from .text import Text

# import sys


LOG_LEVEL = logging.INFO

# LOG_FORMAT = '%(relativeCreated)d %(levelname)-8s: %(name)-26s %(message)s'
# logging.basicConfig(level=LOG_LEVEL, format=LOG_FORMAT, stream=sys.stdout)


# ----------------------------------------------------------
# LOGGING
# ----------------------------------------------------------


class Logger(object):
    """A logger class with color that can handle console and gui cases."""

    COLORS = {
        'debug': 'green',
        'info': 'cyan',
        'warning': 'yellow',
        'error': 'red',
        'exception': 'red',
        'critical': 'red',
    }

    def __init__(self, name, options=None):
        """Class constructor.

        :param name: name of the logger
        :type name: str

        :param options: optional argparse options
        :type options: :py:class:`argparse.Namespace`
        """
        self.name = name
        self.log = logging.getLogger(name)
        self.log.level = LOG_LEVEL
        self.with_color = True
        self.options = options

    @property
    def level(self):
        """Get logging level."""
        return logging.getLevelName(self.log.level)

    @level.setter
    def level(self, value):
        """Set logging level."""
        log_level = {
            'DEBUG': logging.DEBUG,        # 10
            'INFO': logging.INFO,          # 20
            'WARNING': logging.WARNING,    # 30
            'ERROR': logging.ERROR,        # 40
            'EXCEPTION': logging.ERROR,    # 40
            'CRITICAL': logging.CRITICAL,  # 50
        }
        if isinstance(value, str):
            assert value in log_level, 'level not implemented'
            self.log.level = log_level[value]
        elif isinstance(value, int):
            self.log.level = value
        else:
            raise NotImplementedError

    def _dispatch(self, category, msg, *args, **kwargs):
        """Helper function for coloring log msg by type of msg."""
        msg = msg.format(*args, **kwargs)
        if self.with_color:
            msg = Text(msg).colored(self.COLORS[category], attrs=['bold'])
        getattr(self.log, category)(msg)

    def info(self, msg, *args, **kwargs):
        """Log info msg."""
        self._dispatch('info', msg, *args, **kwargs)

    def debug(self, msg, *args, **kwargs):
        """Log debug msg."""
        self._dispatch('debug', msg, *args, **kwargs)

    def warning(self, msg, *args, **kwargs):
        """Log warning msg."""
        self._dispatch('warning', msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        """Log error msg."""
        self._dispatch('error', msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        """Log exception msg."""
        self._dispatch('exception', msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        """Log critical msg."""
        self._dispatch('critical', msg, *args, **kwargs)
