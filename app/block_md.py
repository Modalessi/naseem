import re
from typing import Callable

from enums import BlockType
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_md import text_node_to_html_node, text_to_text_nodes


def md_to_blocks(md: str) -> list[str]:
    blocks = md.split("\n\n")
    blocks = map(lambda b: b.strip(), blocks)
    blocks = filter(lambda b: b != " ", blocks)
    return list(blocks)


def block_to_block_type(block: str) -> BlockType:
    headings = ["# ", "## ", "### ", "#### ", "##### ", "###### "]
    if any(map(block.startswith, headings)):
        return BlockType.HEADING

    if block.startswith("```") and block.endswith("```"):
        return BlockType.CODE

    if all(line.startswith(">") for line in block.split("\n")):
        return BlockType.QUOTE

    if all(line.startswith("* ") or line.startswith("- ") for line in block.split("\n")):
        return BlockType.UNORDERED_LIST

    if all(re.match(r"^\d+. ", line) for line in block.split("\n")):
        return BlockType.ORDERRED_LIST

    return BlockType.PARAGRAPH


def md_to_html_node(md: str) -> HTMLNode:
    blocks = md_to_blocks(md)

    nodes = []
    for block in blocks:
        html_tag = to_html_tag(block)
        nodes.append(html_tag)

    return ParentNode("div", nodes)


def text_to_html_nodes(text: str):
    text_nodes = text_to_text_nodes(text)
    html_nodes = list(map(text_node_to_html_node, text_nodes))
    return html_nodes


def to_html_tag(block: str):
    block_type = block_to_block_type(block)

    if block_type.value == BlockType.HEADING.value:
        return to_heading(block)

    if block_type.value == BlockType.QUOTE.value:
        return to_quote(block)

    if block_type.value == BlockType.UNORDERED_LIST.value:
        return to_list(block, False)

    if block_type.value == BlockType.ORDERRED_LIST.value:
        return to_list(block, True)

    if block_type.value == BlockType.CODE.value:
        return to_code_block(block)

    return to_paragraph(block)


def to_heading(block: str):
    tag = {1: "h1", 2: "h2", 3: "h3", 4: "h4", 5: "h5", 6: "h6"}[block[:6].count("#")]
    value = block.split(" ", 1)[1]
    children = text_to_html_nodes(value)

    return ParentNode(tag, children)


def to_quote(block: str):
    value = ""
    for line in block.split("\n"):
        value += line[1:]

    children = text_to_html_nodes(value)
    return ParentNode("blockquote", children)


def to_list(block: str, ordered: bool):
    items = []

    for line in block.split("\n"):
        items.append(line[2:])

    items_nodes = list(map(lambda i: ParentNode("li", text_to_html_nodes(i)), items))
    return ParentNode("ol" if ordered else "ul", items_nodes)


def to_code_block(block: str):
    value = block[3:-3]
    return LeafNode(value, "code")


def to_paragraph(block: str):
    children = text_to_html_nodes(block)
    return ParentNode("p", children)
