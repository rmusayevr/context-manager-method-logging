import logging
import sys
from contextlib import contextmanager


@contextmanager
def log(level):
    logger = logging.getLogger()
    original_level = logger.getEffectiveLevel()
    logger.setLevel(level)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(level)
    logger.addHandler(stream_handler)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    stream_handler.setFormatter(formatter)
    try:
        yield logger
    finally:
        logger.removeHandler(stream_handler)
        logger.setLevel(original_level)
