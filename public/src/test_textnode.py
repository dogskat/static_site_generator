import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_values_are_none(self):
        node = TextNode()
        self.assertIsNone(node.text)
        self.assertIsNone(node.text_type)
        self.assertIsNone(node.url)


if __name__ == "__main__":
    unittest.main()
