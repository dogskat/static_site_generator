import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_tag_value_not_none(self):
        node = HTMLNode("p", "this is a paragraph")
        self.assertIsNotNone(node.tag)
        self.assertIsNotNone(node.value)

    def test_tag_children_not_none(self):
        node = HTMLNode("div", children=["div", "p"])
        self.assertIsNotNone(node.tag)
        self.assertIsNotNone(node.children)

    def test_values_are_none(self):
        node = HTMLNode("a", props={"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.tag, "a")
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')


if __name__ == "__main__":
    unittest.main()

