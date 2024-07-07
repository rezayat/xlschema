import os
import pytest
from xlschema.ext.appsettings import SettingsParser
from conftest import CONFIG_YAML
'''
var     | init  <  default  <  yaml  <  env  <  cmdline
-----------------------------------------------------------
color   |          blue        green    orange
foo     |          bar                          hello
robot   |          small       large    huge    massive
size    |          100         150
timeout |                      10
is_true | X                    True
'''
@pytest.fixture(scope='function')
def options():
    os.environ['FAVCOLOR'] = 'orange'
    os.environ['ROBOT'] = 'huge'
    with open(CONFIG_YAML) as cfg:
        parser = SettingsParser(yaml_file=cfg)
        opt = parser.add_argument
        opt('--color', default='blue', env_var='FAVCOLOR')
        opt('--foo', default='bar')
        opt('--robot', default='small', env_var='ROBOT')
        opt('--size', type=int, default=100)
        opt('--is_true', type=bool)
        options = parser.parse_args([
            '--foo',    'hello',
            '--robot',  'massive',
        ])
    yield options

def test_no_yaml():
    parser = SettingsParser()
    opt = parser.add_argument
    opt('--foo', default='bar')
    options = parser.parse_args([
        '--foo',    'hello',
    ])
    assert options.foo == 'hello'

def test_override_by_yaml(options):
    assert options.color == 'orange'

def test_override_by_cmdline(options):
    assert options.foo == 'hello'

def test_cmdline_overrides_env(options):
    assert options.robot == 'massive'

def test_default(options):
    assert options.size == 150

def test_yaml_not_injected(options):
    with pytest.raises(AttributeError):
        timeout = options.timeout

def test_cmdline_no_default_yaml_injected(options):
    assert options.is_true

def test_env_set_yaml_file():
    os.environ['APP_SETTINGS_YAML'] = CONFIG_YAML
    parser = SettingsParser()
    opt = parser.add_argument
    opt('--color', default='blue')
    opt('--foo', default='bar')
    options = parser.parse_args([
        '--foo',    'hello',
    ])
    assert options.color == 'green'
