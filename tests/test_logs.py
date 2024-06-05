import logging
from datetime import datetime

from pytemplate.service.logs import log


def test_log_debug_level():
    with log(logging.DEBUG) as logger:
        assert logger.level == logging.DEBUG

    assert logger.level == logging.WARNING


def test_log_info_level():
    with log(logging.INFO) as logger:
        assert logger.level == logging.INFO

    assert logger.level == logging.WARNING


def test_log_warning_level():
    with log(logging.WARNING) as logger:
        assert logger.level == logging.WARNING

    assert logger.level == logging.WARNING


def test_log_error_level():
    with log(logging.ERROR) as logger:
        assert logger.level == logging.ERROR

    assert logger.level == logging.WARNING


def test_log_critical_level():
    with log(logging.CRITICAL) as logger:
        assert logger.level == logging.CRITICAL

    assert logger.level == logging.WARNING


def test_log_debug_level_sys(caplog):
    with log(logging.DEBUG) as logger:
        logger.debug("This is a debug message")

    assert "This is a debug message" in caplog.text


def test_log_info_level_sys(caplog):
    with log(logging.INFO) as logger:
        logger.info("This is an info message")

    assert "This is an info message" in caplog.text


def test_log_warning_level_sys(caplog):
    with log(logging.WARNING) as logger:
        logger.warning("This is a warning message")

    assert "This is a warning message" in caplog.text


def test_log_error_level_sys(caplog):
    with log(logging.ERROR) as logger:
        logger.error("This is an error message")

    assert "This is an error message" in caplog.text


def test_log_critical_level_sys(caplog):
    with log(logging.CRITICAL) as logger:
        logger.critical("This is a critical message")

    assert "This is a critical message" in caplog.text
