#!/usr/bin/env python3
"""A module to manage sql dependencies between files.

The DependencyManager
- creates a graph of dependencies
- loads sql objects in the right order (based on fkey relationships)
"""
import logging
import os


class DependencyManager(object):
    """Manages & optimizes dependencies between model artifacts."""

    def __init__(self, path, prefix='--REQ', suffix='.sql'):
        """Initialize DependencyManager.

        :param path: path to folders where sql files reside
        :type path: str

        :param prefix: (default --REQ) commented sentinel at top of sql file
        :para prefix: str

        :param suffix: (default .sql) type of file for dependency mgmt
        :para type: str
        """
        self.path = path
        self.prefix = prefix
        self.suffix = suffix
        self.pathmap = {}
        self.depmap = {}
        self.groups = []
        self.log = logging.getLogger(self.__class__.__name__)

    def makedirs(self):
        """Creates default structure."""

    def process(self):
        """Main process."""
        self.build()
        self.resolve()
        self.load()

    def _parse_file_deps(self, path):
        """Parse dependencies from a file.

        :param path: path of file to parse
        :type path: str

        :rtype: tuple(namepath) of dependencies
        """
        assert path.endswith(self.suffix), path
        deps = []
        with open(path) as open_file:
            for line in open_file.readlines():
                if line.startswith(self.prefix):
                    entry = line.lstrip(self.prefix).strip()
                    deps.append(entry)
        return tuple(deps)

    def build(self):
        """Build dependencies."""
        for directory in os.listdir(self.path):
            dirpath = os.path.join(self.path, directory)
            # print('dirpath:', dirpath)
            if os.path.isdir(dirpath):
                self.pathmap[directory] = dirpath
                for fname in os.listdir(dirpath):

                    filepath = os.path.join(dirpath, fname)
                    # print('filepath: ', filepath)
                    if os.path.isfile(filepath) and filepath.endswith('.sql'):
                        name, _ = os.path.splitext(os.path.basename(filepath))
                        namepath = os.path.join(directory, name)
                        # print('namepath: ', namepath)
                        self.pathmap[namepath] = filepath
                        deps = self._parse_file_deps(filepath)
                        self.depmap[namepath] = deps

    def resolve(self):
        """Dependency resolver.

        Operates on ``depmap``, a dependency dictionary in which the values are
        the dependencies of their respective keys.

        Returns a list of sets which show the order in which "tasks" can
        be "done" and Groups tasks that can be done simultaneously.

        Usage::

            print(depends(dict(
                a=('b','c'),
                b=('c','d'),
                e=(),
                f=('c','e'),
                g=('h','f'),
                i=('f',))))

            => [set(['h', 'c', 'e', 'd']),
                set(['b', 'f']),
                set(['a', 'i', 'g'])]
        """
        deps = dict((key, set(self.depmap[key])) for key in self.depmap)
        results = []
        while deps:
            # values not in keys (items without dep)
            dset = set(i for v in list(deps.values())
                       for i in v) - set(deps.keys())
            # and keys without value (items without dep)
            dset.update(k for k, v in list(deps.items()) if not v)
            # can be done right away
            results.append(dset)
            # and cleaned up
            deps = dict(((k, v - dset) for k, v in list(deps.items()) if v))
        self.groups = results

    def load(self):
        """Load all dependencies in the right order."""
        self.log.debug('loading dependencies')
        for group in self.groups:
            for name in group:
                path = self.pathmap[name]
                self.log.debug('loading: %s', name)
                self.load_file(path)

    def load_file(self, path):
        """Load single sql file into postgres."""
        if os.path.exists(path) and path.endswith('.sql'):
            self.cmd('psql -f {}'.format(path), fail_ok=True)
        else:
            self.log.error('cannot load %s', path)

    def load_dir(self, path):
        """Load all sql files in a given folder in alphabetical order."""
        for filename in os.listdir(path):
            target = os.path.join(path, filename)
            self.load_file(target)

    def cmd(self, shell_cmd, fail_ok=True):
        """Run and log shell command securely.

        :param shell_cmd: shell command string to execute
        :param fail_ok: if True, don't raise exceptions on command failure
        :raises subprocess.CalledProcessError: if command fails and fail_ok=False
        :raises ValueError: if command is invalid
        """
        self.log.debug("Executing command: %s", shell_cmd)

        try:
            # Use shlex.split for safe command parsing
            import shlex
            import subprocess

            cmd_args = shlex.split(shell_cmd)
            result = subprocess.run(
                cmd_args,
                check=False,  # Handle manually
                capture_output=True,
                text=True,
                timeout=300  # 5 minute timeout
            )

            if result.returncode == 0:
                if result.stdout:
                    self.log.debug("Command output: %s", result.stdout.strip())
                return result
            else:
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


# if __name__ == '__main__':
#     DependencyManager('data/schema').process()
