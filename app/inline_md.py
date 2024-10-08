import re

from enums import TextType
from htmlnode import HTMLNode, LeafNode
from textnode import TextNode


def text_node_to_html_node(text_node: TextNode) -> HTMLNode:
    acceptable_types = [TextType.TEXT, TextType.BOLD, TextType.ITALIC, TextType.CODE, TextType.LINK, TextType.IMAGE]

    if text_node.text_type not in acceptable_types:
        raise ValueError("text type is not supported")

    value = text_node.text
    return {
        TextType.TEXT: LeafNode(value),
        TextType.BOLD: LeafNode(value, "b"),
        TextType.ITALIC: LeafNode(value, "i"),
        TextType.CODE: LeafNode(value, "code"),
        TextType.LINK: LeafNode(value, "a", {"href": text_node.url}),
        TextType.IMAGE: LeafNode(value, "img", {"src": text_node.url}),
    }[text_node.text_type]


def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_nodes = []
        sections = node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Invalid markdown, formatted section not closed")

        for i, v in enumerate(sections):
            if v == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(v, TextType.TEXT))
            else:
                split_nodes.append(TextNode(v, text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_images(text: str) -> list[tuple]:
    img_regex = r"!\[(.*?)\]\((.*?)\)"
    imgs = re.findall(img_regex, text)
    return imgs


def extract_links(text: str) -> list[tuple]:
    links_regex = r"(?<!!)\[(.*?)\]\((.*?)\)"
    links = re.findall(links_regex, text)
    return links


def split_nodes_imgs(old_nodes: list[TextNode]):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            new_nodes.extend(split_node_imgs(node))

    return new_nodes


def split_node_imgs(node: TextNode) -> list[TextNode]:
    nodes = []
    imgs = extract_images(node.text)
    text = node.text
    for img in imgs:
        alt = img[0]
        url = img[1]
        md_stx = f"![{alt}]({url})"
        splits = text.split(md_stx, 1)
        nodes.append(TextNode(splits[0], TextType.TEXT))
        nodes.append(TextNode(alt, TextType.IMAGE, url))
        text = splits[1]

    if text != "":
        nodes.append(TextNode(text, TextType.TEXT))
    return nodes


def split_nodes_links(old_nodes: list[TextNode]) -> list[TextNode]:
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            new_nodes.extend(split_node_links(node))

    return new_nodes


def split_node_links(node: TextNode) -> list[TextNode]:
    nodes = []
    links = extract_links(node.text)
    text = node.text
    for link in links:
        link_text = link[0]
        url = link[1]
        md_stx = f"[{link_text}]({url})"
        splits = text.split(md_stx, 1)
        nodes.append(TextNode(splits[0], TextType.TEXT))
        nodes.append(TextNode(link_text, TextType.LINK, url))
        text = splits[1]

    if text != "":
        nodes.append(TextNode(text, TextType.TEXT))
    return nodes


def text_to_text_nodes(text: str) -> list[TextNode]:
    nodes = [TextNode(text, TextType.TEXT)]

    nodes = split_nodes_imgs(nodes)
    nodes = split_nodes_links(nodes)
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)

    return nodes
