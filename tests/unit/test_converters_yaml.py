from pathlib import Path

import pytest
import yaml

from conftest import (SKIP_ERROR_FILES, YL_DIR,
                      exists, get_app, check, cleanup)


def test_malformed_yaml_error():
    with pytest.raises(yaml.YAMLError):
        app = get_app('node_malformed.yml')

def test_reading_long_yaml_format():
    app = get_app('node_long_data.yml')
    app.write('sql/sqlite')
    check('node_long_data_sqlite.sql')

def test_reading_minimal_yaml_format():
    app = get_app('node_minimal.yml')
    app.write('sql/sqlite')
    check('node_minimal_sqlite.sql')

def test_reading_all_yaml():
    for f in Path(YL_DIR).iterdir():
        fname = str(f.name)
        if fname in SKIP_ERROR_FILES:
            continue
        app = get_app(fname)
        app.write('sql/sqlite')
        name = '{}_sqlite.sql'.format(f.stem)
        assert exists(name)
    cleanup()
