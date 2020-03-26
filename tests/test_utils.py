import unittest
from pypis.services import utils


class TestVersionComparison(unittest.TestCase):
    def test_version_comparison_00(self):
        cmp = utils.compare_versions("0.0.1", "0.0.2")
        self.assertEqual(cmp, -1)

    def test_version_comparison_01(self):
        cmp = utils.compare_versions("0.2", "0.0.9999")
        self.assertEqual(cmp, 1)

    def test_version_comparison_02(self):
        cmp = utils.compare_versions("0.0.1.0", "0.0.1")
        self.assertEqual(cmp, 0)

    def test_version_comparison_03(self):
        cmp = utils.compare_versions("0.1.dev1", "0.1.dev0")
        self.assertEqual(cmp, 1)

    def test_version_comparison_04(self):
        cmp = utils.compare_versions("0.1.0", "0.1.dev0")
        self.assertEqual(cmp, 1)

    def test_version_comparison_05(self):
        cmp = utils.compare_versions("0.0.5a4", "0.0.5a1")
        self.assertEqual(cmp, 1)


class TestSortListByVersion(unittest.TestCase):
    def test_sort_by_version_00(self):
        should_be = ["0.4.2.dev0", "0.4.2", "0.42", "42.0"]
        sorted = utils.sort_list_by_version(["0.4.2", "0.4.2.dev0", "0.42", "42.0"])
        self.assertEqual(sorted, should_be)

    def test_sort_by_version_01(self):
        should_be = [ "1.0.42", "1.4.20", "1.4.21", "42.0.1"]
        sorted = utils.sort_list_by_version(["1.0.42", "1.4.20", "1.4.21", "42.0.1"])
        self.assertEqual(sorted, should_be)

    def test_sort_by_version_02(self):
        should_be = [ "42.0.1", "1.4.21", "1.4.20", "1.0.42"]
        sorted = utils.sort_list_by_version(["1.0.42", "1.4.20", "1.4.21", "42.0.1"], reverse=True)
        self.assertEqual(sorted, should_be)