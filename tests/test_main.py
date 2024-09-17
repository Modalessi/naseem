import unittest

from app.main import extract_title


class TestMain(unittest.TestCase):

    def test_extract_title(self):
        md = "# this is a title"
        self.assertEqual(extract_title(md), "this is a title")

        md = "this is some markdown"
        self.assertEqual(extract_title(md), "Untitled")
