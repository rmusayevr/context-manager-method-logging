import logging
from datetime import datetime

import pytest

from pytemplate.domain.models import LogLevel
from pytemplate.domain.validators import validate_log_level
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


def test_log_level_values():
    assert LogLevel.DEBUG.value == logging.DEBUG
    assert LogLevel.INFO.value == logging.INFO
    assert LogLevel.WARNING.value == logging.WARNING
    assert LogLevel.ERROR.value == logging.ERROR
    assert LogLevel.CRITICAL.value == logging.CRITICAL


def test_valid_log_level():
    @validate_log_level(LogLevel.INFO)
    def test_function():
        return "Function executed"

    assert test_function() == "Function executed"


def test_invalid_log_level_type_str():
    with pytest.raises(TypeError) as exc_info:

        @validate_log_level("INFO")
        def test_func_invalid_type():
            return "This should fail"

        test_func_invalid_type()

    assert str(exc_info.value) == "Level argument must be of type LogLevel, not <class 'str'>"


def test_invalid_log_level_type_int():
    with pytest.raises(TypeError) as exc_info:

        @validate_log_level(50)
        def test_func_invalid_type():
            return "This should fail"

        test_func_invalid_type()

    assert str(exc_info.value) == "Level argument must be of type LogLevel, not <class 'int'>"
