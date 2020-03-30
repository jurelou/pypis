import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient

from pypis.main import app


client = TestClient(app)


class TestSimpleApi(unittest.TestCase):
    def test_get_package(self):
        pass
