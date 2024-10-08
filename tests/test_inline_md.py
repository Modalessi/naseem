import unittest

from app.enums import TextType
from app.htmlnode import LeafNode
from app.inline_md import (
    extract_images,
    extract_links,
    split_nodes_delimiter,
    split_nodes_imgs,
    split_nodes_links,
    text_node_to_html_node,
    text_to_text_nodes,
)
from app.textnode import TextNode


class TestMain(unittest.TestCase):

    def test_text_node_to_html_node(self):
        bold_node = TextNode("hello world", TextType.BOLD)
        html_bold_node = LeafNode("hello world", "b")
        self.assertEqual(text_node_to_html_node(bold_node), html_bold_node)

        italic_node = TextNode("hello world", TextType.ITALIC)
        html_italic_node = LeafNode("hello world", "i")
        self.assertEqual(text_node_to_html_node(italic_node), html_italic_node)

        code_node = TextNode("print('hello world')", TextType.CODE)
        html_code_node = LeafNode("print('hello world')", "code")
        self.assertEqual(text_node_to_html_node(code_node), html_code_node)

        link_node = TextNode("click me", TextType.LINK, "www.google.com")
        html_link_code = LeafNode("click me", "a", {"href": "www.google.com"})
        self.assertEqual(text_node_to_html_node(link_node), html_link_code)

        image_node = TextNode("", TextType.IMAGE, "https://picsum.photos/200/300")
        html_image_node = LeafNode("", "img", {"src": "https://picsum.photos/200/300"})
        self.assertEqual(text_node_to_html_node(image_node), html_image_node)

    def test_split_text_node(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

        node2 = TextNode("This is text with a `code block` word, also another `huge code block`", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node2], "`", TextType.CODE)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word, also another ", TextType.TEXT),
                TextNode("huge code block", TextType.CODE),
            ],
            new_nodes,
        )

        node3 = TextNode("This is text with a **bold** word, also another **BOLD**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node3], "**", TextType.BOLD)

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" word, also another ", TextType.TEXT),
                TextNode("BOLD", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_extract_images(self):
        md_text = """Example with Two Images
        Here are two images displayed using Markdown:
        ![img1](https://example.com/image1.jpg)
        ![img2](https://example.com/image2.png)
        """

        imgs = extract_images(md_text)

        self.assertEqual(
            imgs,
            [
                ("img1", "https://example.com/image1.jpg"),
                ("img2", "https://example.com/image2.png"),
            ],
            imgs,
        )

    def test_extract_links(self):
        md_text = """Example with Two Links
        Here are two links:
        [link1](https://example.com/page1)
        [link2](https://example.com/page2)
        """

        links = extract_links(md_text)

        self.assertEqual(
            links,
            [
                ("link1", "https://example.com/page1"),
                ("link2", "https://example.com/page2"),
            ],
            links,
        )

    def test_split_nodes_links(self):
        node = TextNode(
            "This is text with a link [to google](https://www.google.dev) and [to youtube](https://www.youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_links([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to google", TextType.LINK, "https://www.google.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com"),
            ],
            new_nodes,
        )

    def test_split_nodes_imgs(self):
        node = TextNode(
            "This is text with imgs ![to google](https://www.google.dev) and ![to youtube](https://www.youtube.com)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_imgs([node])

        self.assertEqual(
            new_nodes,
            [
                TextNode("This is text with imgs ", TextType.TEXT),
                TextNode("to google", TextType.IMAGE, "https://www.google.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com"),
            ],
            new_nodes,
        )

    def test_text_to_text_nodes(self):
        md = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://google.com)"
        nodes = text_to_text_nodes(md)

        self.assertEqual(
            nodes,
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://google.com"),
            ],
        )
