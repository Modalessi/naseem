import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):

    def test_probs_to_html(self):
        node = HTMLNode("a", "click here", None, {"href": "www.google.com"})
        self.assertEqual(node.probs_to_html(), 'href="www.google.com"')

    def test_repr(self):
        node = HTMLNode(tag="h1", value="this is some text")

        self.assertEqual(node.__repr__(), "HTMLNode(tag=h1, value=this is some text, children=None, probs=None)")
