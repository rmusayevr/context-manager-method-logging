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


def test_log_debug_level_sys(capsys):
    with log(logging.DEBUG) as logger:
        logger.debug("This is a debug message")

    captured = capsys.readouterr()
    assert "This is a debug message" in captured.out


def test_log_info_level_sys(capsys):
    with log(logging.INFO) as logger:
        logger.info("This is an info message")

    captured = capsys.readouterr()
    assert "This is an info message" in captured.out


def test_log_warning_level_sys(capsys):
    with log(logging.WARNING) as logger:
        logger.warning("This is a warning message")

    captured = capsys.readouterr()
    assert "This is a warning message" in captured.out


def test_log_error_level_sys(capsys):
    with log(logging.ERROR) as logger:
        logger.error("This is an error message")

    captured = capsys.readouterr()
    assert "This is an error message" in captured.out


def test_log_critical_level_sys(capsys):
    with log(logging.CRITICAL) as logger:
        logger.critical("This is a critical message")

    captured = capsys.readouterr()
    assert "This is a critical message" in captured.out


def test_log_datetime(capsys):
    with log(logging.CRITICAL) as logger:
        logger.critical("This is a critical message")

    captured = capsys.readouterr()
    captured_date_format = captured.out.split(" - ")[0]
    response = bool(datetime.strptime(captured_date_format, "%Y-%m-%d %H:%M:%S,%f"))
    assert response == True
