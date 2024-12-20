import unittest

from textnode import TextNode, TextType
from htmlnode import LeafNode, text_node_to_html_node


class TestNodeToHtmlNode(unittest.TestCase):
    def test_text_value(self):
        node = TextNode("This is a pure text node", TextType.NORMAL)
        leaf_node = text_node_to_html_node(node)
        self.assertIsNone(leaf_node.tag)
        self.assertEqual(leaf_node.value, "This is a pure text node")


    def test_bold_tag(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.tag, "b")
        self.assertEqual(leaf_node.value, "This is a bold text node")


    def test_italice_tag(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.tag, "i")
        self.assertEqual(leaf_node.value, "This is an italic text node")


    def test_code_tag(self):
        node = TextNode("print('This code statement')", TextType.CODE)
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.tag, "code")
        self.assertEqual(leaf_node.value, "print('This code statement')")


    def test_anchor_tag(self):
        node = TextNode("Link to Google", TextType.LINK, url="https://www.google.com")
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.tag, "a")
        self.assertEqual(leaf_node.value, "Link to Google")
        self.assertEqual(leaf_node.props, {"href": "https://www.google.com"} )
        self.assertEqual(leaf_node.to_html(), '<a href="https://www.google.com">Link to Google</a>')


    def test_image_tag(self):
        node = TextNode("Grapefruit slice atop a pile of other slices", TextType.IMAGE, url="/media/cc0-images/grapefruit-slice-332-332.jpg")
        leaf_node = text_node_to_html_node(node)
        self.assertEqual(leaf_node.tag, "img")
        self.assertEqual(leaf_node.value, "")
        self.assertEqual(leaf_node.props, {"src": "/media/cc0-images/grapefruit-slice-332-332.jpg", "alt": "Grapefruit slice atop a pile of other slices"})
        self.assertEqual(leaf_node.to_html(), '<img src="/media/cc0-images/grapefruit-slice-332-332.jpg" alt="Grapefruit slice atop a pile of other slices"></img>')


    def test_invalid_texttype(self):
        with self.assertRaises(Exception):
            node = TextNode("", TextType.UNKNOWN)
            text_node_to_html_node(node)


if __name__ == "__main__":
    unittest.main()
