import logging
from typing import List, Optional

from loralogger.handlers import LogToESHandler

# adapted from https://dock2learn.com/tech/create-a-reusable-logger-factory-for-python-projects/


class LoraLogger:
    @staticmethod
    def __create_logger(
        label: Optional[str],
        format: Optional[str],
        date_format: Optional[str],
        level: Optional[str],
        log_to_es: bool = False,
        log_to_console: bool = False,
        log_to_syslog: bool = False,
    ) -> logging.Logger:
        logger_name: str = label or "loralogger"

        logger_format: str = format or "| %(levelname)-9s | %(asctime)s | %(message)s"
        date_format = date_format or "%Y-%m-%dT%H:%M:%S"

        logger_level: str = level or "DEBUG"

        logger_mapper: dict = {
            "DEBUG": logging.DEBUG,
            "debug": logging.DEBUG,
            "INFO": logging.INFO,
            "info": logging.INFO,
            "WARNING": logging.WARNING,
            "warning": logging.WARNING,
            "ERROR": logging.ERROR,
            "error": logging.ERROR,
            "CRITICAL": logging.CRITICAL,
            "critical": logging.CRITICAL,
        }

        logger_handlers: List = []

        if log_to_es:
            es_handlers = LogToESHandler(label=logger_name)
            logger_handlers.append(es_handlers)

        if log_to_console:
            console_handler = logging.StreamHandler()
            logger_handlers.append(console_handler)

        if log_to_syslog:
            syslog_handler = logging.handlers.SysLogHandler()  # type: ignore
            logger_handlers.append(syslog_handler)

        # We create our own Logger instance here, and set the default level.
        logger: logging.Logger = logging.getLogger(logger_name)
        logger.setLevel(logger_mapper[logger_level])

        # Add handlers for it, including the log format
        for handler in logger_handlers:
            formatter = logging.Formatter(fmt=logger_format, datefmt=date_format)
            handler.setFormatter(formatter)

            logger.addHandler(handler)

        return logger

    @staticmethod
    def get_logger(
        label: str,
        format: Optional[str] = None,
        date_format: Optional[str] = None,
        level: Optional[str] = None,
        log_to_es: bool = False,
        log_to_console: bool = False,
        log_to_syslog: bool = False,
    ) -> logging.Logger:
        """Static method to generate a logger with specific label and format."""

        logger = LoraLogger.__create_logger(
            label,
            format,
            date_format,
            level,
            log_to_es,
            log_to_console,
            log_to_syslog,
        )

        return logger
