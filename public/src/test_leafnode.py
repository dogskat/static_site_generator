import unittest

from htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_leaf_no_tag(self):
        node = LeafNode(value="This is a paragraph of text.")
        self.assertIsNone(node.tag)
        self.assertIsNotNone(node.value)
        self.assertEqual(node.to_html(), node.value)

    def test_leaf_no_props(self):
        node = LeafNode("This is a paragraph of text.", "p")
        self.assertIsNotNone(node.tag)
        self.assertIsNotNone(node.to_html(), '<p>This is a paragraph of text.</p>')

    def test_leaf_with_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.to_html(), '<a href="https://www.google.com">Click me!</a>')

    def test_value_error_for_no_value(self):
        node = LeafNode(tag="a", value=None, props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')


if __name__ == "__main__":
    unittest.main()

