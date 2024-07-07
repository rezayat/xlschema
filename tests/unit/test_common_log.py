import pytest

from xlschema.common.log import Logger


class Application:
    def __init__(self):
        self.log = Logger(self.__class__.__name__)
        self.msg = 'hello'

    def speak(self):
        self.log.info(self.msg)
        self.log.debug(self.msg)
        self.log.warning(self.msg)
        self.log.error(self.msg)
        self.log.critical(self.msg)

    def throw(self):
        try:
            1/0
        except:
            self.log.exception(self.msg)
            raise

yaml_config = '''
disable_existing_loggers: false
version: 1
formatters:
  short:
    format: '%(asctime)s %(levelname)s %(name)s: %(message)s'
handlers:
  console:
    level: INFO
    formatter: short
    class: logging.StreamHandler
loggers:
  default:
    level: ERROR
    handlers: [console]
  plugins:
    level: INFO
    handlers: [console]
    propagate: false
'''


def test_yaml_log_config():
    import logging
    import logging.config
    import yaml

    config = yaml.load(yaml_config, Loader=yaml.SafeLoader)
    logging.config.dictConfig(config)
    logging.info('hello')

def test_log_level():
    app = Application()
    app.speak()
    # INFO is default
    assert app.log.level == 'INFO'
    app.log.level = 'DEBUG'
    app.speak()
    assert app.log.level == 'DEBUG'
    app.log.level = 30
    app.speak()
    assert app.log.level == 'WARNING'
    app.log.level = 100
    app.speak()
    # break it
    with pytest.raises(NotImplementedError):
        app.log.level = {'hello': None}

def test_log_exception():
    app = Application()
    with pytest.raises(ZeroDivisionError):
        app.throw()
