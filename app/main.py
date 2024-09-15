from enums import TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    acceptable_types = [TextType.TEXT, TextType.BOLD, TextType.ITALIC, TextType.CODE, TextType.LINK, TextType.IMAGE]

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
    }[text_node.text_type.value]


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            new_nodes.extend(split_text_node(node, delimiter, text_type))

    return new_nodes


def split_text_node(node: TextNode, delimiter: str, text_type: TextType) -> list[TextNode]:
    nodes = []

    text = node.text
    current = ""
    open_delimiter = False
    for _, c in enumerate(text):
        if c != delimiter:
            current += c
        else:
            if open_delimiter:
                new_node = TextNode(current, text_type)
                nodes.append(new_node)
                current = ""
                open_delimiter = False
            else:
                new_node = TextNode(current, TextType.TEXT)
                nodes.append(new_node)
                current = ""
                open_delimiter = True

    if current != "":
        nodes.append(TextNode(current, text_type if open_delimiter else TextType.TEXT))

    return nodes


def main():
    node = TextNode("This is text with a `code block` word", TextType.TEXT)
    new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
    print(*new_nodes, sep="\n")


if __name__ == "__main__":
    main()
