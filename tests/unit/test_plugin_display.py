import pytest

from conftest import (
    shell,
    XLSCHEMA,
)

# can be skipped with: pytest -k-slow
pytestmark = pytest.mark.slow()

def test_plugin_display():
    shell([XLSCHEMA, 'display'])

def test_plugin_display_options():
    shell([XLSCHEMA, 'display',
        '--offset 25',
        '--qualify',
    ])
