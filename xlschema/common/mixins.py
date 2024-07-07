"""Common mixin classes."""
import os


class CommandMixin:
    """Mixin class for shell operations."""

    def cmd(self, shellcmd, *args, **kwds):
        """Utility function to call shell commands."""
        shellcmd = shellcmd.format(*args, **kwds)
        self.log.warning(shellcmd)
        os.system(shellcmd)
