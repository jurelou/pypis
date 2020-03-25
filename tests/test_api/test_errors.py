import unittest

from fastapi.testclient import TestClient

from pypis.main import app


client = TestClient(app)


class TestErrors(unittest.TestCase):
    def test_404(self):
        response = client.get("/this/does/not/exist")
        self.assertEqual(response.status_code, 404)
        self.assertTrue("errors" in response.json())
