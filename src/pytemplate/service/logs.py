import logging
import sys
from contextlib import contextmanager
from logging.config import dictConfig

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "stdout": {
            "class": "logging.StreamHandler",
            "stream": "ext://sys.stdout",
        },
    },
    "loggers": {
        "root": {
            "level": "WARNING",
            "handlers": ["stdout"],
        }
    },
}

dictConfig(LOGGING)



@contextmanager
def log(level):
    logger = logging.getLogger()
    original_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    try:
        yield logger
    finally:
        logger.setLevel(original_level)
