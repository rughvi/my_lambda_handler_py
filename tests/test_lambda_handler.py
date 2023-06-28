import unittest
from datetime import datetime, timedelta, timezone
import lambda_handler


class TestLambdaHandler(unittest.TestCase):
    def test_event_too_old(self):
        result = lambda_handler.lambda_handler({
            "time": (datetime.utcnow() - timedelta(minutes=10)).replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        }, {})
        self.assertFalse(result)

    def test_event_not_too_old(self):
        result = lambda_handler.lambda_handler({
            "time": (datetime.utcnow() - timedelta(minutes=2)).replace(tzinfo=timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        }, {})
        self.assertTrue(result)
