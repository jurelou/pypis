from datetime import datetime
from pydantic.error_wrappers import ValidationError
import unittest
from pypis.api.models.releases import ReleaseFromPypi, ReleasePrivateUpload


class TestReleasesFromPypi(unittest.TestCase):
    def setUp(self):
        self.base_release = {
            "filename": "release-filename.txt",
            "packagetype": "sdist",
            "author": "me",
            "md5_digest": "cm9vdAo",
            "url": "http://example.com",
            "version": "42",
            "upload_time": datetime.now(),
            "upload_time_iso_8601": datetime.now(),
        }

    def test_release_from_pypi_00(self):
        release = self.base_release
        try:
            ReleaseFromPypi(**release)
        except Exception as err:
            self.fail("test_release_from_pypi_00 should not have raised {}".format(err))

    def test_release_from_pypi_01(self):
        release = self.base_release
        release["packagetype"] = "source"
        with self.assertRaises(ValidationError):
            ReleaseFromPypi(**release)

    def test_release_from_pypi_02(self):
        release = self.base_release
        release["packagetype"] = "source"
        release["pyversion"] = "2"
        try:
            ReleaseFromPypi(**release)
        except Exception as err:
            self.fail("test_release_from_pypi_00 should not have raised {}".format(err))

    def test_release_from_pypi_03(self):
        release = self.base_release
        release["packagetype"] = "sdist"
        release["pyversion"] = "2"
        with self.assertRaises(ValidationError):
            ReleaseFromPypi(**release)

    def test_release_from_pypi_04(self):
        release = self.base_release
        release["packagetype"] = "sdist"
        try:
            r = ReleaseFromPypi(**release)
        except Exception as err:
            self.fail("test_release_from_pypi_00 should not have raised {}".format(err))

        self.assertEqual(r.python_version, "source")


class TestReleasesPrivateUpload(unittest.TestCase):
    def setUp(self):
        self.base_release = {
            "filename": "release-filename.txt",
            "packagetype": "sdist",
            "author": "me",
            "md5_digest": "cm9vdAo",
            "url": "http://example.com",
            "version": "42",
        }

    def test_private_release_00(self):
        release = self.base_release
        release["author_email"] = "invalidemail"

        with self.assertRaises(ValidationError):
            ReleasePrivateUpload(**release)
