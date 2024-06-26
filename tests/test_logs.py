import logging
from datetime import datetime
from io import StringIO
from logging.config import dictConfig
from unittest.mock import patch

import pytest

from pytemplate.configurator.settings.base import LOGGING
from pytemplate.domain.validators import validate_log_level
from pytemplate.entrypoints.cli.main import main
from pytemplate.service.logs import log
from src.pytemplate.domain.models import LogLevel


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


dictConfig(LOGGING)


def test_log_datetime(caplog):
    with log(logging.CRITICAL) as logger:
        logger.critical("This is a critical message")

    captured_date_format = [record.asctime for record in caplog.records][0]
    response = bool(datetime.strptime(captured_date_format, "%Y-%m-%d %H:%M:%S,%f"))
    assert response == True


def test_log_level_values():
    assert LogLevel.DEBUG.value == logging.DEBUG
    assert LogLevel.INFO.value == logging.INFO
    assert LogLevel.WARNING.value == logging.WARNING
    assert LogLevel.ERROR.value == logging.ERROR
    assert LogLevel.CRITICAL.value == logging.CRITICAL


def test_log_level_names():
    assert str(LogLevel.DEBUG) == "LogLevel.DEBUG"
    assert str(LogLevel.INFO) == "LogLevel.INFO"
    assert str(LogLevel.WARNING) == "LogLevel.WARNING"
    assert str(LogLevel.ERROR) == "LogLevel.ERROR"
    assert str(LogLevel.CRITICAL) == "LogLevel.CRITICAL"


def dummy_log_function():
    kwargs = {"level": "DEBUG"}
    with log(**kwargs) as logger:
        logger.debug("Hey there")
        return "Validation passed successfully!"


def test_validate_log_level_valid():
    response = dummy_log_function()
    assert response == "Validation passed successfully!"


def test_validate_log_level_invalid_str():
    with pytest.raises(ValueError):
        kwargs = {"level": "INVALID_LEVEL"}
        with log(**kwargs) as logger:
            pass


def test_validate_log_level_invalid_int():
    with pytest.raises(ValueError):
        kwargs = {"level": 10}
        with log(**kwargs) as logger:
            pass


def test_validate_log_level_invalid_none():
    with pytest.raises(ValueError):
        kwargs = {"level": None}
        with log(**kwargs) as logger:
            pass


@pytest.mark.parametrize(
    "user_input, expected_output",
    [
        (["DEBUG"], "Main worked successfully!"),
        (["INFO"], "Main worked successfully!"),
        (["WARNING"], ""),
        (["ERROR"], ""),
        (["CRITICAL"], ""),
    ],
)
def test_main(user_input, expected_output, capsys):
    with patch("builtins.input", side_effect=user_input):
        main()
        captured = capsys.readouterr()
        assert expected_output in captured.out
