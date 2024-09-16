from block_md import *
from enums import TextType
from inline_md import split_nodes_delimiter, text_to_text_nodes
from textnode import TextNode


def main():
    md = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the **first** list item in a list block
* This is a list item
* This is another list item"""

    md_in_html = """<div>
<h1>This is a heading</h1>

<p>This is a paragraph of text. It has some <b>bold</b> and <i>italic</i> words inside of it.</p>

<ul>
<li>This is the <b>first</b> list item in a list block</li>
<li>This is a list item</li>
<li>This is another list item</li>
</ul>
</div>"""

    html_node = md_to_html_node(md)
    print(html_node.to_html())


if __name__ == "__main__":
    main()
