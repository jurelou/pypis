import unittest
from pypis.services import html


class TestHtmlService(unittest.TestCase):
    def test_build_html_text_00(self):
        should_be = """\
<!DOCTYPE html>
<html>
  <head>
    <title></title>
  </head>
  <body>
    
  </body>
</html>
"""
        page = html.build_html_text()
        self.assertEqual(page, should_be)

    def test_build_html_text_01(self):
        should_be = """\
<!DOCTYPE html>
<html>
  <head>
    <title>sometitle</title>
  </head>
  <body>
    
  </body>
</html>
"""
        page = html.build_html_text(title="sometitle")
        self.assertEqual(page, should_be)

    def test_build_html_text_02(self):
        should_be = """\
<!DOCTYPE html>
<html>
  <head>
    <title>sometitle</title>
  </head>
  <body>
    somecontent
  </body>
</html>
"""
        page = html.build_html_text(title="sometitle", body="somecontent")
        self.assertEqual(page, should_be)

    def test_build_html_text_03(self):
        should_be = """\
<!DOCTYPE html>
<html>
  <head>
    <title>sometitle</title>
  </head>
  <body>
    multiline
    content
    
  </body>
</html>
"""

        page = html.build_html_text(title="sometitle", body="multiline\ncontent\n")
        self.assertEqual(page, should_be)

    def test_dicts_to_anchors_00(self):
        pass
