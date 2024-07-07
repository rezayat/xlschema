"""A very basic configuration module."""

import os
from collections import OrderedDict
from pathlib import Path

# from .writers.abstract import SchemaWriter

from mako.lookup import TemplateLookup
from sqlalchemy.engine.url import make_url

# ----------------------------------------------------------
# CONFIGURATION
# ----------------------------------------------------------


class Config:
    """Basic configuration class."""

    # paths
    XLSCHEMA_PKG = Path(__file__).absolute().parent
    XLSCHEMA_PROJECT = XLSCHEMA_PKG.parent
    RESOURCES = XLSCHEMA_PROJECT / 'xlschema' / 'resources'
    TEMPLATES = RESOURCES / 'templates'
    APP_PKG = TEMPLATES / 'pkg'

    # ROOT = Path('.')
    # OUTPUT = ROOT / 'tests' / 'data' / 'output'

    LOCAL_DIR = Path('.xlschema')
    LOCAL_OUTPUT = str(LOCAL_DIR / 'data' / 'output')

    DB_URI = os.getenv('DB_URI', 'sqlite:///tests/data/db/test.sqlite')
    db_uri = make_url(DB_URI)

    TEMPLATE_COMMENT_OFFSET = 55
    TEMPLATE_ENV = TemplateLookup(
        directories=[str(TEMPLATES)],
        module_directory='/tmp/mako_modules')

    ENUMS_SHEET = 'ENUMs'
    ACTIONS = ['noprefix']  # acceptable actions
    METAFIELDS = [
        'description',
        'action',
        'category',
        'constraint',
        'default',
        'required',
        'index',
        'length',
        'type',
        'name']
    # app-level
    WRITERS = OrderedDict()  # type: OrderedDict[str, SchemaWriter]


def register(cls):
    """Class decorator to register the writer class."""
    path = '{}/{}'.format(cls.file_suffix, cls.method)
    Config.WRITERS[path] = cls
    return cls
