import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):

    def test_probs_to_html(self):
        node = HTMLNode("a", "click here", None, {"href": "www.google.com"})
        self.assertEqual(node.probs_to_html(), 'href="www.google.com"')

    def test_repr(self):
        node = HTMLNode(tag="h1", value="this is some text")

        self.assertEqual(node.__repr__(), "HTMLNode(tag=h1, value=this is some text, children=None, probs=None)")


class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("this is a leaf node")
        self.assertEqual(node.to_html(), "this is a leaf node")

    def test_to_html_with_tag(self):
        node = LeafNode("this is a leaf node", "h1")
        self.assertEqual(node.to_html(), "<h1>this is a leaf node</h1>")

    def test_to_html_with_probs(self):
        node = LeafNode("this is a leaf node", "h1", {"id": "title", "class": "text"})
        self.assertEqual(node.to_html(), '<h1 id="title" class="text">this is a leaf node</h1>')

    def test_to_html_with_empty_value(self):
        node = LeafNode(None)
        with self.assertRaises(ValueError):
            node.to_html()
