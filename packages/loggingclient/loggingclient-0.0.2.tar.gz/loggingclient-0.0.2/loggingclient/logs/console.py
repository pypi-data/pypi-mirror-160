"""Console logs formatter."""

import logging
from logging.config import dictConfig

import pylogctx

DEFAULT_LOG_FORMAT = "{levelname}: [{pathname}:{funcName}] {message}"


class ContextFormatter(logging.Formatter):
    """Add context to the message, if any."""

    def __init__(self, fmt=None, datefmt=None, style="{"):
        super(ContextFormatter, self).__init__(fmt=fmt, datefmt=datefmt, style=style)

    def format(self, record):
        """Format record with showing existing context."""
        msg = super(ContextFormatter, self).format(record)
        context = pylogctx.context.as_dict()
        if not context:
            return msg

        return "{msg} (context: {context!r})".format(msg=msg, context=context)


class ErrorFilter(logging.Filter):
    """Pass only messages with severity ERROR or higher."""

    def filter(self, record):
        """Filter records only with error level."""
        return super(ErrorFilter, self).filter(record) and record.levelno >= logging.ERROR


class InfoFilter(logging.Filter):
    """Pass only messages with severity lower than ERROR."""

    def filter(self, record):
        """Filter records only with error level."""
        return super(InfoFilter, self).filter(record) and record.levelno < logging.ERROR


def configure(level: int, log_format: str = DEFAULT_LOG_FORMAT):
    """Configure loggers."""
    log_format = DEFAULT_LOG_FORMAT if log_format is None else log_format
    dictConfig(
        {
            "version": 1,
            "disable_existing_loggers": False,
            "formatters": {"context": {"()": ContextFormatter, "format": log_format}},
            "filters": {"info": {"()": InfoFilter}, "error": {"()": ErrorFilter}},
            "handlers": {
                "info": {
                    "class": "logging.StreamHandler",
                    "formatter": "context",
                    "stream": "ext://sys.stdout",
                    "filters": ["info"],
                },
                "error": {
                    "class": "logging.StreamHandler",
                    "formatter": "context",
                    "stream": "ext://sys.stderr",
                    "filters": ["error"],
                },
            },
            "root": {"level": level, "handlers": ["info", "error"]},
        }
    )
