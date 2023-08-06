import logging
from unittest import TestCase
from unittest.mock import patch, ANY, sentinel

import pylogctx

from loggingclient.logs.console import ContextFormatter, ErrorFilter, InfoFilter, configure


class ConsoleLogsTestCase(TestCase):
    def setUp(self) -> None:
        self.dict_config = patch("loggingclient.logs.console.dictConfig").start()
        self.record = logging.LogRecord(
            "log.record",
            logging.INFO,
            "path/name.py",
            42,
            "logging message",
            (),
            None,
            func="function_name",
        )
        self.formatter = ContextFormatter()

    def test_configure(self):
        configure(sentinel.log_level)

        self.dict_config.assert_called_once_with(
            {
                "version": 1,
                "disable_existing_loggers": False,
                "formatters": {
                    "context": {
                        "()": ContextFormatter,
                        "format": "{levelname}: [{pathname}:{funcName}] {message}",
                    }
                },
                "filters": {"info": {"()": ANY}, "error": {"()": ANY}},
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
                "root": {"level": sentinel.log_level, "handlers": ["info", "error"]},
            }
        )

    def test_context_formatter(self):
        with pylogctx.context(extra=sentinel.extra):
            msg = self.formatter.format(self.record)

        self.assertEqual("logging message (context: {'extra': sentinel.extra})", msg)

    def test_context_formatter_no_context(self):
        msg = self.formatter.format(self.record)
        self.assertEqual("logging message", msg)

    def test_info_filter(self):
        self.assertFalse(InfoFilter().filter(logging.makeLogRecord({"levelno": logging.ERROR})))
        self.assertFalse(InfoFilter().filter(logging.makeLogRecord({"levelno": logging.CRITICAL})))
        self.assertTrue(InfoFilter().filter(logging.makeLogRecord({"levelno": logging.WARNING})))
        self.assertTrue(InfoFilter().filter(logging.makeLogRecord({"levelno": logging.INFO})))
        self.assertTrue(InfoFilter().filter(logging.makeLogRecord({"levelno": logging.DEBUG})))

    def test_error_filter(self):
        self.assertTrue(ErrorFilter().filter(logging.makeLogRecord({"levelno": logging.ERROR})))
        self.assertTrue(ErrorFilter().filter(logging.makeLogRecord({"levelno": logging.CRITICAL})))
        self.assertFalse(ErrorFilter().filter(logging.makeLogRecord({"levelno": logging.WARNING})))
        self.assertFalse(ErrorFilter().filter(logging.makeLogRecord({"levelno": logging.INFO})))
        self.assertFalse(ErrorFilter().filter(logging.makeLogRecord({"levelno": logging.DEBUG})))
