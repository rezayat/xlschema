"""Commonly useful context managers."""
import logging
import time


class Timer(object):
    """A timer as a context manager."""

    def __init__(self, log=None):
        """Class constructor.

        :param log: optional logger to use
        :type log: :py:class:`xlschema.common.log.Logger`
        """
        self.log = log if log else logging.getLogger(self.__class__.__name__)
        self.fmt = "END: {:.3f} seconds"
        self.start = None
        self.end = None

    def __enter__(self):
        """Set the start time."""
        self.log.info('START')
        self.start = time.process_time()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """Set the end time."""
        self.end = time.process_time()
        msg = self.fmt.format((self.end - self.start))
        self.log.info(msg)
