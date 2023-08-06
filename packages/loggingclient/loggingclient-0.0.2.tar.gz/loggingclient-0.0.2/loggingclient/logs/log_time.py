"""Utilities for code execution time profiling."""

import contextlib
import logging
import time

import pylogctx

__all__ = ["log_time"]


@contextlib.contextmanager
def log_time(message: str, logger: logging.Logger, level: int = logging.DEBUG):
    """Measures execution time of context manager's code block.

    Writes execution time in seconds to the log after passed message.

    Args:
        message: Message to be displayed after code block executed.
        logger: existing logger to make logs flow without cuts.
        level: Logging level threshold.

    Yields:
        Instance of PostMessage inner class for additional messaging.

    """
    start_time = time.monotonic()
    try:
        yield
    finally:
        exec_time = time.monotonic() - start_time
        with pylogctx.context(exec_time=exec_time):
            logger.log(level, message)
