import os

from conftest import TEST_DB


def test_config_environ_baseline():
    from xlschema.config import Config

    assert not os.getenv('DB_URI')
    assert Config.DB_URI == TEST_DB

def test_config_environ_external():
    MY_DB = 'sqlite:///my.db'
    os.environ['DB_URI'] = MY_DB

    from xlschema.config import Config

    # doesn't pick up from import must be set outside:
    # DB_URI=sqlite:///my.db pytest tests/test_config.py
    assert not Config.DB_URI == MY_DB

def test_config_db():
    from xlschema.config import Config

    db = Config.db_uri
    assert db.drivername == 'sqlite'
    assert db.username == None
    assert db.password == None
    assert db.host == None
    assert db.port == None
    assert db.database == TEST_DB.replace('sqlite:///', '')
