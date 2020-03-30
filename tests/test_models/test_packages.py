from pydantic.error_wrappers import ValidationError
import unittest
from pypis.api.models.packages import PackageCreate, PackageUpload


class TestPackagesUpload(unittest.TestCase):
    def setUp(self):
        self.base_package = {
            "name": "dummypackage",
            "classifiers": [],
            "author": "me",
            "version": "1.0",

            "metadata_version": "2.0",
            "filetype": "sdist",
            "md5_digest": "cm9vdAo"
        }

    def test_package_upload_00(self):
        package = self.base_package
        try:
            PackageUpload(**self.base_package)
        except Exception as err:
            self.fail("test_package_upload_00 should not have raised {}".format(err))

    def test_package_upload_01(self):
        package = self.base_package
        package.pop("md5_digest")
        with self.assertRaises(ValidationError):
            PackageUpload(**package)

    def test_package_upload_02(self):
        package = self.base_package
        package["filetype"] = "source"
        with self.assertRaises(ValidationError):
            PackageUpload(**package)

    def test_package_upload_03(self):
        package = self.base_package
        package["filetype"] = "source"
        package["pyversion"] = "4.2"
        try:
            PackageUpload(**self.base_package)
        except Exception as err:
            self.fail("test_package_upload_03 should not have raised {}".format(err))

    def test_package_upload_04(self):
        package = self.base_package
        package.pop("author")
        with self.assertRaises(ValidationError):
            PackageUpload(**package)

    def test_package_upload_05(self):
        package = self.base_package
        p = PackageUpload(**self.base_package)
        self.assertEqual(p.pyversion, "source")


class TestPackagesCreate(unittest.TestCase):
    def setUp(self):
        self.base_package = {
            "name": "dummypackage",
            "classifiers": [],
            "author": "me",
            "version": "1.0"
        }

    def test_package_00(self):
        try:
            PackageCreate(**self.base_package)
        except Exception as err:
            self.fail("test_package_00 should not have raised {}".format(err))

    def test_package_01(self):
        package = self.base_package
        package["name"] = "invalidchars~~"
        with self.assertRaises(ValidationError):
            PackageCreate(**package)

    def test_package_02(self):
        package = self.base_package
        package["version"] = " 0.1.2"
        with self.assertRaises(ValidationError):
            PackageCreate(**package)

    def test_package_03(self):
        package = self.base_package
        package["summary"] = """
        multiline
        summary
        """
        with self.assertRaises(ValidationError):
            PackageCreate(**package)

    def test_package_04(self):
        package = self.base_package
        package["summary"] = "A" * 600
        with self.assertRaises(ValidationError):
            PackageCreate(**package)

    def test_package_05(self):
        package = self.base_package
        package["description_content_type"] = "invalid"
        with self.assertRaises(ValidationError):
            PackageCreate(**package)

    def test_package_06(self):
        package = self.base_package
        package["author_email"] = "invalidemail"
        with self.assertRaises(ValidationError):
            PackageCreate(**package)

    def test_package_07(self):
        package = self.base_package
        package["author_email"] = "me@example.com"
        package["description_content_type"] = "text/plain"
        package["home_page"] = "http://example.com"
        package["license"] = "MIT"
        package["package_url"] = "http://package.com"
        package["project_url"] = "http://project.com"
        package["summary"] = "test project"
        package["description"] = "yes"
        package["keywords"] = "ok"
        try:
            PackageCreate(**package)
        except Exception as err:
            self.fail("test_package_07 should not have raised {}".format(err))
