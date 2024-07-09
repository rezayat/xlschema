import logging
import logging.config
import yaml

yaml_config = '''
logging:
    version: 1
    disable_existing_loggers: false

    formatters:
        standard:
            format: '%(asctime)s [%(levelname)-8s] %(name)s.%(funcName)s: %(message)s'
            datefmt: '%H:%M:%S'
        short:
            format: '%(asctime)s [%(levelname)-8s] %(name)s: %(message)s'
            datefmt: '%Y-%m-%d %H:%M:%S'
        extended:
            format: '%(asctime)s [%(levelname)-8s] %(name)-26s: %(message)s'
            datefmt: '%Y-%m-%d %H:%M:%S'

    handlers:
        console:
            level: INFO
            formatter: short
            class: logging.StreamHandler
            stream: ext://sys.stdout

        default:
            level: INFO
            formatter: standard
            class: logging.StreamHandler

        info_file_handler:
            class: logging.handlers.RotatingFileHandler
            level: INFO
            formatter: standard
            filename: ./tests/data/logs/info.log
            maxBytes: 10485760 # 10MB
            backupCount: 20
            encoding: utf8

        error_file_handler:
            class: logging.handlers.RotatingFileHandler
            level: ERROR
            formatter: standard
            filename: ./tests/data/logs/errors.log
            maxBytes: 10485760 # 10MB
            backupCount: 20
            encoding: utf8

    loggers:
        plugins:
            level: WARN
            handlers: [console]
            propagate: false

    root:
        level: INFO
        handlers: [console, info_file_handler, error_file_handler]
        propogate: false
'''

def test_dictconfig():
    config = yaml.safe_load(yaml_config)
    logging.config.dictConfig(config['logging'])
    log = logging.getLogger()
    log.info('This is a info msg')
    log.debug('This is a debug msg')
    log.warning('This is a warning msg')
    log.error('This is an error')
    log.critical('This is a critical error')
