import json
import logging
from unittest import TestCase
from unittest import mock
from unittest.mock import patch

from loggingclient.logs import log_time
from loggingclient.logs import logs
from loggingclient.logs.logs import LogConfig


class LogTimeTestCase(TestCase):
    def setUp(self) -> None:
        self.logger = mock.Mock(spec=logging.Logger)
        self.logger.__str__ = lambda: ""

    def tearDown(self) -> None:
        patch.stopall()

    def test_util_log_time(self):
        with log_time.log_time("message", logger=self.logger, level=logging.INFO):
            pass

        self.logger.log.assert_called_once_with(logging.INFO, "message")

    def test_util_log_time_with_exception_in_body(self):
        with self.assertRaises(AttributeError):
            with log_time.log_time("msg", logger=self.logger, level=logging.INFO):
                raise AttributeError()
