"""Common templating operations."""
import hashlib
import logging
import os
from pathlib import Path
from typing import Any

from mako.lookup import TemplateLookup
from mako.template import Template


class TemplateEntry:
    """Represents an item (file or folder) to be processed."""

    def __init__(self, entry: str, root: str) -> None:
        """Initialize TemplateEntry instances."""
        self.entry = Path(entry)
        self.root = Path(root)
        self.path = self.root / self.entry

    @property
    def is_abbrev(self) -> bool:
        """Returns True if entry is an abbreviation.

        case is abbreviated::

            format == 'sql/sqlite'
        """
        entry = str(self.entry)
        ext, *_ = entry.split('/')
        subpath = Path('{entry}.{ext}'.format(entry=entry, ext=ext))
        path = self.root / subpath
        return all([
            self.entry.suffix == '',
            self.entry.parts[0] != 'pkg',
            not self.path.is_file(),
            not self.path.is_dir(),
            path.is_file(),
        ])

    @property
    def is_file(self) -> bool:
        """Returns True if entry is an existing file.

        case is file path::

            format == 'sql/**/sqlite.sql'
        """
        return all([
            self.entry.suffix != '',
            self.entry.parts[0] != 'pkg',
            self.path.is_file(),
            not self.path.is_dir(),
        ])

    @property
    def is_dir(self) -> bool:
        """Returns True if entry is a directory.

        case is directory path::

            format == 'sql/**/pgmodels'
        """
        return all([
            self.entry.suffix == '',
            self.entry.parts[0] != 'pkg',
            not self.path.is_file(),
            self.path.is_dir(),
        ])

    @property
    def is_pkg(self) -> bool:
        """Returns True if entry is a namespace package.

        case is namespace package::

            format == 'pkg/**/<namespace>'
        """
        return all([
            self.entry.suffix == '',
            self.entry.parts[0] == 'pkg',
            not self.path.is_file(),
            self.path.is_dir(),
        ])


class TemplateEngine:
    """General Template Engine Manager."""

    def __init__(self, templates: str, output: str) -> None:
        """Initialize class."""
        self.templates = Path(templates)
        self.output = Path(output)
        self.env = TemplateLookup(
            directories=[templates], module_directory='/tmp/mako_modules')
        self.log = logging.getLogger(self.__class__.__name__)

    def render(self, entry: str, **kwds: Any) -> None:
        """Picks method based on shape of entry."""
        _entry = TemplateEntry(entry, str(self.templates))
        if _entry.is_abbrev:
            self.log.info('is_abbrev <- %s', entry)
            self.render_from_abbrev(entry, **kwds)
        elif _entry.is_file:
            self.log.info('is_file <- %s', entry)
            self.render_from_file(entry, **kwds)
        elif _entry.is_dir:
            self.log.info('is_dir <- %s', entry)
            self.render_from_dir(entry, **kwds)
        elif _entry.is_pkg:
            self.log.info('is_pkg <- %s', entry)
            self.render_from_pkg(entry, **kwds)
        else:
            raise NotImplementedError

    def render_from_abbrev(self, entry: str, **kwds: Any) -> None:
        """Render from abbreviation."""
        ext, *_ = entry.split('/')
        path = '{entry}.{ext}'.format(entry=entry, ext=ext)
        self.render_from_file(path, **kwds)
        # self.render_template_from_lookup(path, **kwds)

    def render_from_file(self, entry: str, **kwds: Any) -> None:
        """Render from file."""
        self._render_from_file(Path(entry), None, **kwds)

    def render_from_dir(self, entry: str, **kwds: Any) -> None:
        """Render from directory (recursive)."""
        self._render_from_dir(Path(entry), **kwds)

    def render_from_pkg(self, entry: str, **kwds: Any) -> None:
        """Render from namespace pkg."""
        self._render_from_dir(Path(entry), **kwds)

    # ===================================================================

    def render_template_from_string(self, string: str, **kwds: Any) -> str:
        """Render template string and return result."""
        return self.render_mako(string, **kwds)

    def render_template_from_lookup(self, path: str, **kwargs: Any) -> str:
        """Render from lookup source directories."""
        template = self.env.get_template(path)
        return template.render(**kwargs)

    # ===================================================================

    def _render_from_dir(self, directory: Path, **kwds: Any) -> None:
        """Render templates from source directory."""
        self.log.debug('directory: %s', directory)
        path_dir = self.templates / directory
        for root, _, files in os.walk(str(path_dir)):
            self.log.debug('root: %s', root)
            base = Path(root)
            for fname in files:
                src = base / fname
                self.log.debug('src: %s', src)
                target = src.relative_to(self.templates)
                self.log.debug('target: %s', target)
                dst = self.output / target
                self.log.debug('dst: %s', dst)
                self._render_from_file(target, dst, **kwds)

    def _render_from_file(self, src: Path, dst: Path = None, **kwds: Any) -> None:
        """Render from source to destination path."""
        src_path = self.templates / src
        template = src_path.read_text()
        rendered = self.render_template_from_string(template, **kwds)
        if not dst:
            dst = self.output / src
        else:
            dst = Path(dst)
        self.log.debug('dst: %s', dst)
        if not dst.parent.exists():
            self.log.debug('making: %s', dst.parent)
            dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(rendered)
        self.log.info('rendered: %s', dst)

    @staticmethod
    def render_mako(template: str, **kwds: Any) -> str:
        """Render Mako template."""
        return Template(template).render(**kwds)

    @staticmethod
    def hashed(content: str) -> str:
        """Return md5 hexdigest of string content."""
        return hashlib.md5(content.encode('utf-8')).hexdigest()
