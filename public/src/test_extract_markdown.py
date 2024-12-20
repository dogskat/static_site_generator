import unittest

from textnode import TextType, TextNode
from inline_markdown import (
    split_nodes_delimiter,
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
    markdown_to_blocks,
    block_to_block_type,
)

markdown_text = \
"""
# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
"""


class TestTextNode(unittest.TestCase):
    def test_code_block(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode('This is text with a ', TextType.TEXT, None),
            TextNode('code block', TextType.CODE, None),
            TextNode(' word', TextType.TEXT, None)
        ] 
        self.assertEqual(new_nodes, expected_nodes)

    def test_italic_block(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected_nodes = [
            TextNode('This is text with an ', TextType.TEXT, None),
            TextNode('italic', TextType.ITALIC, None),
            TextNode(' word', TextType.TEXT, None)
        ] 
        self.assertEqual(new_nodes, expected_nodes)

    def test_bold_block(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode('This is text with a ', TextType.TEXT, None),
            TextNode('bold', TextType.BOLD, None),
            TextNode(' word', TextType.TEXT, None)
        ] 
        self.assertEqual(new_nodes, expected_nodes)

    def test_double_code_block(self):
        node = TextNode("This is text with a `code block1` word and `code block2` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        expected_nodes = [
            TextNode('This is text with a ', TextType.TEXT, None),
            TextNode('code block1', TextType.CODE, None),
            TextNode(' word and ', TextType.TEXT, None),
            TextNode('code block2', TextType.CODE, None),
            TextNode(' word', TextType.TEXT, None),
        ] 
        self.assertEqual(new_nodes, expected_nodes)

    def test_double_italic_block(self):
        node = TextNode("This is text with an *italic1* word and *italic2* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        expected_nodes = [
            TextNode('This is text with an ', TextType.TEXT, None),
            TextNode('italic1', TextType.ITALIC, None),
            TextNode(' word and ', TextType.TEXT, None),
            TextNode('italic2', TextType.ITALIC, None),
            TextNode(' word', TextType.TEXT, None),
        ] 
        self.assertEqual(new_nodes, expected_nodes)

    def test_double_bold_block(self):
        node = TextNode("This is text with a **bold1** word and **bold2** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        expected_nodes = [
            TextNode('This is text with a ', TextType.TEXT, None),
            TextNode('bold1', TextType.BOLD, None),
            TextNode(' word and ', TextType.TEXT, None),
            TextNode('bold2', TextType.BOLD, None),
            TextNode(' word', TextType.TEXT, None),
        ] 
        self.assertEqual(new_nodes, expected_nodes)

    def test_bold_and_italic_block(self):
        node = TextNode("This is text with a **bold** word and *italic* word", TextType.TEXT)
        nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        expected_nodes = [
            TextNode('This is text with a ', TextType.TEXT, None),
            TextNode('bold', TextType.BOLD, None),
            TextNode(' word and ', TextType.TEXT, None),
            TextNode('italic', TextType.ITALIC, None),
            TextNode(' word', TextType.TEXT, None),
        ] 
        self.assertEqual(new_nodes, expected_nodes)

    def test_no_matching_closing_delimeter(self):
        with self.assertRaises(Exception):
            node = TextNode("This is text with a **bold word", TextType.TEXT)
            new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_extract_markdown_images(self):
        img_text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        img_extracts = extract_markdown_images(img_text)
        test1 = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertEqual(img_extracts, test1)

    def test_extract_markdown_links(self):
        link_text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        link_extract = extract_markdown_links(link_text)
        test2 = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertEqual(link_extract, test2)

    def test_split_nodes_link(self):
        link_node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([link_node])
        test_nodes = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
            ),
        ]
        self.assertEqual(new_nodes, test_nodes)

    def test_split_nodes_image(self):
        img_node = TextNode(
            "This is text with an image ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([img_node])
        test_nodes = [
            TextNode("This is text with an image ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode(
                "obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
            ),
        ]
        self.assertEqual(new_nodes, test_nodes)

    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_links(self):
        node = TextNode(
            "This is text with a [link](https://boot.dev) and [another link](https://blog.boot.dev) with text that follows",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "https://blog.boot.dev"),
                TextNode(" with text that follows", TextType.TEXT),
            ],
            new_nodes,
        )
    def test_text_to_textnodes(self):
        nodes = text_to_textnodes(
            "This is **text** with an *italic* word and a `code block` and an ![image](https://i.imgur.com/zjjcJKZ.png) and a [link](https://boot.dev)"
        )
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

    def test_markdown_to_block(self):
        blocks = markdown_to_blocks(markdown_text)
        self.assertListEqual(
            [
                '# This is a heading',
                'This is a paragraph of text. It has some **bold** and *italic* words inside of it.',
                '* This is the first list item in a list block\n* This is a list item\n* This is another list item'
            ],
            blocks,
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_heading_block_type(self):
        h1 = "# Heading level 1"
        h6 = "###### Heading level 6"
        value = block_to_block_type(h1)
        self.assertEqual("heading", value)
        value = block_to_block_type(h6)
        self.assertEqual("heading", value)

    def test_code_block_type(self):
        code_block = "```\nx = 'Hello World\nprint(x)\n```"
        value = block_to_block_type(code_block)
        self.assertEqual("code", value)

    def test_line_quote_block_type(self):
        blockquote = "> Dorothy followed her through many rooms"
        value = block_to_block_type(blockquote)
        self.assertEqual("quote", value)

    def test_unordered_list_block_type(self):
        unordered_list = "* list item\n* item2\n* item3"
        value = block_to_block_type(unordered_list)
        self.assertEqual("unordered_list", value)

        unordered_list = "- list item\n- item2\n- item3"
        value = block_to_block_type(unordered_list)
        self.assertEqual("unordered_list", value)

    def test_ordered_list_block_type(self):
        ordered_list = "1. First item\n2. Second item\n3. Third item"
        value = block_to_block_type(ordered_list)
        self.assertEqual("ordered_list", value)

    def test_paragraph_block_type(self):
        paragraph = "Some line of text"
        value = block_to_block_type(paragraph)
        self.assertEqual("paragraph", value)

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), "heading")
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), "code")
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), "quote")
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), "unordered_list")
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), "ordered_list")
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), "paragraph")


if __name__ == "__main__":
    unittest.main()

