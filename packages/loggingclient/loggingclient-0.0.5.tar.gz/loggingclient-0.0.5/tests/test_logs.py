import logging
from pathlib import Path
from unittest import TestCase
from unittest.mock import patch

from loggingclient import logs
from loggingclient.logs.logs import LogConfig


class LogsTestCase(TestCase):
    def setUp(self):
        self.console_config = patch("loggingclient.logs.logs.console.configure").start()
        # self.stackdriver_config = patch("loggingclient.logs.logs.container_engine.configure").start()

        self.silenced_loggers = ["google.cloud.pubsub_v1"]

    def assert_loggers_silenced(self, level=logging.WARNING, loggers=None):
        if loggers is None:
            loggers = self.silenced_loggers
        for name in loggers:
            logger = logging.getLogger(name)
            self.assertEqual(logger.level, level)

    def test_namespace_package(self):
        self.assertFalse((Path(logs.__file__).parent.parent / "__init__.py").exists())

    def test_invalid_level(self):
        with self.assertRaises(ValueError):
            logs.configure_logs("INVALID")

        self.console_config.assert_not_called()

    def test_default_config(self):
        logs.configure_logs()
        self.console_config.assert_called_once_with(logging.INFO, log_format=None)
        self.assert_loggers_silenced()

    def test_legacy_default_config(self):
        logs.configure_logs(use_cloud_logging=False)
        self.console_config.assert_called_once_with(logging.INFO, log_format=None)
        self.assert_loggers_silenced()

    def test_default_config_explicit_level(self):
        logs.configure_logs("WARNING")
        self.console_config.assert_called_once_with(logging.WARNING, log_format=None)
        self.assert_loggers_silenced(logging.WARNING)

    def test_default_config_numeric_level(self):
        logs.configure_logs(logging.WARNING)
        self.console_config.assert_called_once_with(logging.WARNING, log_format=None)
        self.assert_loggers_silenced(logging.WARNING)

    def test_silence_custom_logger(self):
        logs.configure_logs(silence=["custom.logger.name"])
        self.console_config.assert_called_once_with(logging.INFO, log_format=None)
        self.assert_loggers_silenced(loggers=["custom.logger.name"])
