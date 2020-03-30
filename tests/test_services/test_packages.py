import unittest
from dynaconf import settings
from pypis.services import packages


class TestPackagesServices(unittest.TestCase):
    def test_normalize_package_name_00(self):
        should_be = "testproject"
        self.assertEqual(packages.normalize_package_name("TestProject"), should_be)

    def test_normalize_package_name_01(self):
        should_be = "test-project"
        self.assertEqual(packages.normalize_package_name("Test..._Project"), should_be)

    def test_normalize_package_name_02(self):
        should_be = "-testproject-"
        self.assertEqual(
            packages.normalize_package_name("._-TestProject-_.."), should_be
        )

    def test_is_valid_pep440_specifier_00(self):
        self.assertTrue(packages.is_valid_pep440_specifier(">=4.3.*"))

    def test_is_valid_pep440_specifier_01(self):
        self.assertTrue(packages.is_valid_pep440_specifier("~= 0.9"))

    def test_is_valid_pep440_specifier_02(self):
        self.assertTrue(packages.is_valid_pep440_specifier("==0"))

    def test_is_valid_pep440_specifier_03(self):
        self.assertFalse(packages.is_valid_pep440_specifier("~=1.*"))

    def test_is_valid_pep440_specifier_04(self):
        self.assertFalse(packages.is_valid_pep440_specifier("nope"))

    def test_is_valid_pep440_specifier_05(self):
        self.assertFalse(packages.is_valid_pep440_specifier("1"))

    def test_is_standard_package_00(self):
        self.assertFalse(packages.is_standard_package("mypackage"))

    def test_is_standard_package_01(self):
        self.assertFalse(packages.is_standard_package("gzip.gzip"))

    def test_is_standard_package_03(self):
        self.assertTrue(packages.is_standard_package("unittest"))
