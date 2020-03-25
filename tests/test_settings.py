import unittest
from dynaconf import settings
from pypis.main import app


class TestSettings(unittest.TestCase):
    def test_test_environment(self):
        self.assertEqual(settings.ENV_FOR_DYNACONF, "testing")

    def test_app_name(self):
        self.assertEqual(app.title, "testing-app")
