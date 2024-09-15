from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    acceptable_types = ["text", "bold", "italic", "code", "link", "image"]

    if text_node.text_type not in acceptable_types:
        raise ValueError("text type is not supported")

    value = text_node.text
    return {
        "text": LeafNode(value),
        "bold": LeafNode(value, "b"),
        "italic": LeafNode(value, "i"),
        "code": LeafNode(value, "code"),
        "link": LeafNode(value, "a", {"href": text_node.url}),
        "image": LeafNode("", "img", {"src": text_node.url}),
    }[text_node.text_type]


if __name__ == "__main__":
    node = ParentNode(
        "p",
        [
            LeafNode(tag="b", value="Bold text"),
            LeafNode(tag=None, value="Normal text"),
            LeafNode(tag="i", value="italic text"),
            LeafNode(tag=None, value="Normal text"),
        ],
    )
    print(node.to_html())
