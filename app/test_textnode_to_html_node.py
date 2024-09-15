import unittest

from htmlnode import LeafNode
from main import text_node_to_html_node
from textnode import TextNode


class TestTextNodeToHtmlNode(unittest.TestCase):

    def test_text_node_to_html_node(self):
        bold_node = TextNode("hello world", "bold")
        html_bold_node = LeafNode("hello world", "b")
        self.assertEqual(text_node_to_html_node(bold_node), html_bold_node)

        italic_node = TextNode("hello world", "italic")
        html_italic_node = LeafNode("hello world", "i")
        self.assertEqual(text_node_to_html_node(italic_node), html_italic_node)

        code_node = TextNode("print('hello world')", "code")
        html_code_node = LeafNode("print('hello world')", "code")
        self.assertEqual(text_node_to_html_node(code_node), html_code_node)

        link_node = TextNode("click me", "link", "www.google.com")
        html_link_code = LeafNode("click me", "a", {"href": "www.google.com"})
        self.assertEqual(text_node_to_html_node(link_node), html_link_code)

        image_node = TextNode("", "image", "https://picsum.photos/200/300")
        html_image_node = LeafNode("", "img", {"src": "https://picsum.photos/200/300"})
        self.assertEqual(text_node_to_html_node(image_node), html_image_node)
