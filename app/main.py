from enums import TextType
from inline_md import split_nodes_delimiter, text_to_text_nodes
from textnode import TextNode


def main():
    md = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"

    nodes = text_to_text_nodes(md)

    print(*nodes, sep="\n")


if __name__ == "__main__":
    main()
