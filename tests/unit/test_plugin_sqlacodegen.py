import pytest

from conftest import (
    shell, exists,
    TEST_DB, XLSCHEMA, OUTPUT,
)

SKIP=True

# can be skipped with: pytest -k-slow
pytestmark = pytest.mark.slow()

@pytest.mark.skipif(SKIP, reason="disabled")
def test_plugin_sqlacodegen_all():
    shell([XLSCHEMA,
        '--output', OUTPUT,
        '--prefix', 'test',
        'to_sqla',
        '--uri "{}"'.format(TEST_DB),
        ])
    assert exists('test_sqla_schema.py')

@pytest.mark.skipif(SKIP, reason="disabled")
def test_plugin_sqlacodegen_table():
    shell([XLSCHEMA,
        '--output', OUTPUT,
        '--prefix', 'test',
        'to_sqla',
        '--uri "{}"'.format(TEST_DB),
        'person',
        'vehicle'
        ])
    assert exists('test_sqla_schema.py')

@pytest.mark.skipif(SKIP, reason="disabled")
def test_plugin_sqlacodegen_table_noprefix():
    shell([XLSCHEMA,
        '--output', OUTPUT,
        'to_sqla',
        '--uri "{}"'.format(TEST_DB),
        'person',
        ])
    assert True # placeholder till will do an endswith check
