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


@validate_log_level
def dummy_log_function(**kwargs):
    return "Validation passed successfully!"


def test_validate_log_level_valid():
    kwargs = {"level": LogLevel.DEBUG}
    response = dummy_log_function(**kwargs)

    assert response == "Validation passed successfully!"


def test_validate_log_level_invalid_int():
    kwargs = {"level": 50}
    with pytest.raises(TypeError) as exc_info:
        dummy_log_function(**kwargs)

    assert str(exc_info.value) == "Level argument must be of type LogLevel, not <class 'int'>"


def test_validate_log_level_invalid_str():
    kwargs = {"level": "DEBUG"}
    with pytest.raises(TypeError) as exc_info:
        dummy_log_function(**kwargs)

    assert str(exc_info.value) == "Level argument must be of type LogLevel, not <class 'str'>"


def test_validate_log_level_invalid_none():
    kwargs = {"level": None}
    with pytest.raises(TypeError) as exc_info:
        dummy_log_function(**kwargs)

    assert str(exc_info.value) == "Level argument must be of type LogLevel, not <class 'NoneType'>"


@patch("builtins.input", side_effect=["DEBUG"])
@pytest.mark.usefixtures("caplog")
def test_log_level_debug(mock_input, caplog):
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        main()
        assert "This is a debug message." in caplog.text


@patch("builtins.input", side_effect=["INFO"])
@pytest.mark.usefixtures("caplog")
def test_log_level_info(mock_input, caplog):
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        main()
        assert "This is an informational message." in caplog.text


@patch("builtins.input", side_effect=["WARNING"])
@pytest.mark.usefixtures("caplog")
def test_log_level_warning(mock_input, caplog):
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        main()
        assert "This is a warning message." in caplog.text


@patch("builtins.input", side_effect=["ERROR"])
@pytest.mark.usefixtures("caplog")
def test_log_level_error(mock_input, caplog):
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        main()
        assert "This is an error message." in caplog.text


@patch("builtins.input", side_effect=["CRITICAL"])
@pytest.mark.usefixtures("caplog")
def test_log_level_critical(mock_input, caplog):
    with patch("sys.stdout", new_callable=StringIO) as mock_stdout:
        main()
        assert "This is a critical message." in caplog.text
