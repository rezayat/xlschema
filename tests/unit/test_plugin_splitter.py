import os

import pytest

from xlschema.plugins.splitter import XLSplitter

from conftest import (
    XLSCHEMA_OUT,
    OPTIONS_DEFAULT,
    SPLIT_XLSX, SPLIT_OUT_DIR,
    shell, exists, split_out,
)

# can be skipped with: pytest -k-slow
pytestmark = pytest.mark.slow()

def test_xlsx_splitter():
    splitter = XLSplitter(
        path=SPLIT_XLSX,
        target_sheet='data',
        group_on='category',
        keep_sheets=False,
        options=OPTIONS_DEFAULT,
    )
    splitter.process()
    for f in ['cat', 'cow', 'dog', 'dolphin', 'horse']:
        assert os.path.exists(split_out(f))
    os.system('rm -rf ' + SPLIT_OUT_DIR)

def test_plugin_split():
    shell([XLSCHEMA_OUT, 'split_xlsx',
        '--keep_sheet', 'data',
        '--group_on', 'category',
        '--sheet', 'data',
        SPLIT_XLSX])
    for f in ['cat', 'cow', 'dog', 'dolphin', 'horse']:
        assert os.path.exists(split_out(f))
    os.system('rm -rf ' + SPLIT_OUT_DIR)
