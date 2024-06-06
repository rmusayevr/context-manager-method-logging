from logging.config import dictConfig

from src.pytemplate.configurator.settings.base import LOGGING
from src.pytemplate.domain.models import LogLevel
from src.pytemplate.service.logs import log


def main():
    dictConfig(LOGGING)

    log_level = input("Enter log level (DEBUG/INFO/WARNING/ERROR/CRITICAL): ")
    level = {"level": LogLevel[log_level.upper()]}

    with log(**level) as logging_manager:
        if logging_manager.level == 10:
            logging_manager.debug("This is a debug message.")
        elif logging_manager.level == 20:
            logging_manager.info("This is an informational message.")
        elif logging_manager.level == 30:
            logging_manager.warning("This is a warning message.")
        elif logging_manager.level == 40:
            logging_manager.error("This is an error message.")
        else:
            logging_manager.critical("This is a critical message.")