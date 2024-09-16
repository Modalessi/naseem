import re

from enums import BlockType


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
