import unittest

from block_md import block_to_block_type, md_to_blocks

from app.enums import BlockType


class TestBlockMD(unittest.TestCase):
    def test_md_to_blocks(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""

        blocks = md_to_blocks(md)

        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
            ],
            blocks,
        )

    def test_block_to_block_type(self):
        paragraph = "hello world, this is a paragraph block"
        self.assertEqual(block_to_block_type(paragraph).value, BlockType.PARAGRAPH.value)

        headings = [
            "# heading 1",
            "## heading 2",
            "### heading 3",
            "#### heading 4",
            "##### heading 5",
            "###### heading 6",
        ]
        self.assertTrue(all(block_to_block_type(b).value == BlockType.HEADING.value for b in headings))

        code = "```python\nprint('hello world')```"
        self.assertEqual(block_to_block_type(code).value, BlockType.CODE.value)

        quote = ">this is a quote, you have any problem ?\n>no i dont"
        self.assertEqual(block_to_block_type(quote).value, BlockType.QUOTE.value)

        unordered_list = "- item 1\n- item 2\n- item3"
        self.assertEqual(block_to_block_type(unordered_list).value, BlockType.UNORDERED_LIST.value)

        ordered_list = "1. item 1\n2. item 2\n3. item3"
        self.assertEqual(block_to_block_type(ordered_list).value, BlockType.ORDERRED_LIST.value)
