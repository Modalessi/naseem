from block_md import *
from enums import TextType
from inline_md import split_nodes_delimiter, text_to_text_nodes
from textnode import TextNode


def main():
    md = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
    """

    blocks = md_to_blocks(md)
    print(blocks)


if __name__ == "__main__":
    main()
