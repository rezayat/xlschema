"""Plugins package."""

# core plugin
from .core import CorePlugin

# extra plugins
from .echo import EchoPlugin
from .display import DisplayPlugin
from .sqlacodegen import SqlaCodegenPlugin
from .splitter import SplitterPlugin


REGISTRY = [
    # core
    CorePlugin,
    # extras
    EchoPlugin,
    DisplayPlugin,
    SqlaCodegenPlugin,
    SplitterPlugin,
]


def list_plugins():
    """Retrieves active plugins from registry."""
    return [plugin for plugin in REGISTRY if plugin.is_active]
