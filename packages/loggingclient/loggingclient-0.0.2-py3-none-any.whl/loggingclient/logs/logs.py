"""Logging utilities."""

import logging
from enum import Enum
from typing import Union, Iterable

from . import console

__all__ = ["configure_logs", "SILENCE_LOGGERS", "LogConfig", "set_loggers_level"]
SILENCE_LOGGERS = frozenset(["google.cloud.pubsub_v1", "google.api_core.bidi"])


class LogConfig(Enum):
    """Available log configs."""

    DEFAULT = "DEFAULT"
    CONSOLE = "CONSOLE"


def set_loggers_level(level: Union[int, str], *loggers: str):
    """Set a level for provided loggers.

    It is useful to silence to verbose logs.

    Args:
        level: log level.
        loggers: logger names.

    """
    for logger in loggers:
        logging.getLogger(logger).setLevel(level)


def configure_logs(
    level: Union[int, str] = "INFO",
    *,
    log_config: LogConfig = LogConfig.DEFAULT,
    log_format: str = None,
    silence: Iterable[str] = SILENCE_LOGGERS,
    use_cloud_logging: bool = None,
):
    """Setup logging levels based on verbosity setting.

    Simply run the method as following::

        configure_logs(LOG_LEVEL, logger_config=LogConfig(LOGGER_CONFIG_NAME))

    Args:
        level: minimal allowed log level.
        log_config: logger configuration to use.  Default is console logging.
        log_format: format of the log message. Only for console logging.
        silence: logger names to set the log level at least to "WARNING".
        use_cloud_logging: if True, use stackdriver logging, otherwise
            log to console.  Deprecated, use
            "logger_config=LogConfig.GKE" instead.

    """

    # if use_cloud_logging is not None:
    #    if log_config is not LogConfig.DEFAULT:
    #        raise RuntimeError("Can't use `logger` and `use_cloud_logging` at the same time")
    #    warnings.warn("use_cloud_logging is deprecated, use `logger` argument", DeprecationWarning)
    #    log_config = LogConfig.GKE if use_cloud_logging else LogConfig.CONSOLE

    # Normalize the level
    if not isinstance(level, int):
        level = logging.getLevelName(level)
        if not isinstance(level, int):
            raise ValueError(f"{level} is not a valid level")

    # configure logs with console.configure()
    if log_config is not None:
        console.configure(level, log_format=log_format)
        print("configure logs with console.configure()")

    silence_level = logging.WARNING if level <= logging.WARNING else level
    set_loggers_level(silence_level, *silence)

    print(
        f"end of configure_logs function level: {level} config: {log_config} format: {log_format}"
    )
