import os
import shutil

from block_md import *
from enums import TextType
from inline_md import split_nodes_delimiter, text_to_text_nodes
from textnode import TextNode


def copy_contents(src_dir: str, dest_dir: str):

    # delete public contents
    shutil.rmtree("public")
    os.mkdir("public")

    contents = copy_content_helper(src_dir)

    for file in contents:
        print(f"[ COPIED ] {file.name}")


def copy_content_helper(path: str):
    entites = os.scandir(path)
    contents = []

    for entity in entites:
        entity_relative_path = entity.path.split("/", 1)[1]
        if entity.is_file():
            shutil.copyfile(entity.path, os.path.join("public", entity_relative_path))
            contents.append(entity)
            continue

        os.mkdir(os.path.join("public", entity_relative_path))
        contents.extend(copy_content_helper(entity.path))

    return contents


def main():
    copy_contents("static", "public")


if __name__ == "__main__":
    main()
