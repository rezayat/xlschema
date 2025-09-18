"""Common mixin classes."""
import shlex
import subprocess


class CommandMixin:
    """Mixin class for shell operations."""

    def cmd(self, shellcmd, *args, **kwds):
        """Utility function to call shell commands securely.

        :param shellcmd: shell command string
        :param args: positional arguments for formatting
        :param kwds: keyword arguments for formatting
        :raises subprocess.CalledProcessError: if command fails and fail_ok=False
        :raises ValueError: if command contains unsafe characters
        """
        # Extract special parameters
        fail_ok = kwds.pop('fail_ok', False)
        log_level = kwds.pop('log_level', 'warning')

        # Format the command safely
        try:
            formatted_cmd = shellcmd.format(*args, **kwds)
        except (KeyError, ValueError) as e:
            self.log.error("Invalid command format: %s", e)
            raise ValueError(f"Invalid command format: {e}")

        # Log command execution at appropriate level
        getattr(self.log, log_level)("Executing command: %s", formatted_cmd)

        # Use shlex.split for safe parsing and subprocess.run for execution
        try:
            # Split command safely to handle spaces and quotes
            cmd_args = shlex.split(formatted_cmd)
            result = subprocess.run(
                cmd_args,
                check=False,  # Don't raise exception, handle manually
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if result.returncode == 0:
                if result.stdout:
                    self.log.debug("Command output: %s", result.stdout.strip())
                return result
            else:
                # Command failed
                error_msg = f"Command failed with exit code {result.returncode}: {result.stderr.strip()}"

                if fail_ok:
                    self.log.warning("Command failed (ignoring): %s", error_msg)
                    return result
                else:
                    self.log.error(error_msg)
                    raise subprocess.CalledProcessError(
                        result.returncode, cmd_args, result.stdout, result.stderr
                    )

        except subprocess.TimeoutExpired as e:
            error_msg = f"Command timed out after {e.timeout} seconds"
            if fail_ok:
                self.log.warning("Command timed out (ignoring): %s", error_msg)
                return None
            else:
                self.log.error(error_msg)
                raise
        except (OSError, FileNotFoundError) as e:
            error_msg = f"Invalid command: {e}"
            if fail_ok:
                self.log.warning("Command not found (ignoring): %s", error_msg)
                return None
            else:
                self.log.error(error_msg)
                raise ValueError(error_msg)
