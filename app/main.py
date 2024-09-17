import os
import re
import shutil
from pathlib import Path

from block_md import md_to_html_node


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


def extract_title(md: str) -> str:
    title = re.match(r"^# .+ *\n?", md, flags=re.IGNORECASE)

    if title:
        return title[0][1:].strip()

    return "Untitled"


def generate_pages(dir_path_content, template_path, dest_dir_path):
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)
        if os.path.isfile(from_path) and from_path.endswith(".md"):
            dest_path = Path(dest_path).with_suffix(".html")
            generate_page_helper(from_path, template_path, dest_path)
        else:
            generate_pages(from_path, template_path, dest_path)


def generate_page_helper(from_path: str, template_path: str, dest_path: str):
    md = ""
    with open(from_path, "r", encoding="utf-8") as f:
        md = f.read()

    template = ""
    with open(template_path, "r", encoding="utf-8") as f:
        template = f.read()

    html_node = md_to_html_node(md)
    html = html_node.to_html()
    title = extract_title(md)

    page = template.replace("{{ Title }}", title).replace("{{ Content }}", html)
    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(page)


def main():
    copy_contents("static", "public")
    generate_pages("content", "template.html", "public")


if __name__ == "__main__":
    main()
