"""
Модуль для инициализации настроек логирования
"""

import logging
import logging.config


def init_logging():
    """
    Инициализация логгера
    """
    log_format = f"[%(asctime)s] [ CI/CD server ] [%(levelname)s]:%(name)s:%(message)s"
    formatters = {'basic': {'format': log_format}}
    handlers = {'stdout': {'class': 'logging.StreamHandler', 'formatter': 'basic'}}
    level = 'INFO'
    handlers_names = ['stdout']
    loggers = {'': {'level': level, 'propagate': False, 'handlers': handlers_names}}
    logging.basicConfig(level='INFO', format=log_format)
    log_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': formatters,
        'handlers': handlers,
        'loggers': loggers
    }
    logging.config.dictConfig(log_config)
