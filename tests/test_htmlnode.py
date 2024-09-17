import unittest

from app.htmlnode import HTMLNode, LeafNode, ParentNode


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

    def test_equlitty(self):
        node1 = LeafNode("click me", "a", {"href": "www.google.com"})
        node2 = LeafNode("click me", "a", {"href": "www.google.com"})

        self.assertEqual(node1, node2)


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        simple_node = ParentNode(
            "p",
            [
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
                LeafNode(tag="i", value="italic text"),
                LeafNode(tag=None, value="Normal text"),
            ],
        )

        self.assertEqual(simple_node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

        complex_node = ParentNode(
            "p",
            [
                ParentNode(
                    "ul",
                    [
                        LeafNode("Cofee", "li", probs={"class": "item"}),
                        LeafNode("Tea", "li", probs={"class": "item"}),
                        LeafNode("Milk", "li", probs={"class": "item"}),
                    ],
                ),
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
                LeafNode(tag="i", value="italic text"),
                LeafNode(tag=None, value="Normal text"),
            ],
        )

        correct_html = '<p><ul><li class="item">Cofee</li><li class="item">Tea</li><li class="item">Milk</li></ul><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        self.assertEqual(complex_node.to_html(), correct_html)

    def to_html_with_probs(self):
        node = ParentNode(
            "p",
            [
                LeafNode(tag="b", value="Bold text"),
                LeafNode(tag=None, value="Normal text"),
                LeafNode(tag="i", value="italic text"),
                LeafNode(tag=None, value="Normal text"),
            ],
            probs={"id": "body", "class": "text"},
        )

        self.assertEqual(
            node.to_html(), '<p id="body" class="text"><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>'
        )
