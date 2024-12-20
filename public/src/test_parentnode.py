import unittest

from htmlnode import ParentNode, LeafNode


class TestParentNode(unittest.TestCase):
    def test_tag_assert(self):
        # TODO: test ValueError if no tag
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        node = ParentNode(
            None,
            children,
        )
        # assertRaises(ValueError, <instance creation or .to_html call?>
        self.assertRaises(ValueError, node.to_html)

    def test_children_assert(self):
        # TODO: test ValueError if no child
        node = ParentNode(
            "p",
            None,
        )
        # assertRaises(ValueError, <instance creation or .to_html call?>
        self.assertRaises(ValueError, node.to_html)

    def test_leaf_children(self):
        children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
        ]
        node = ParentNode(
            "p",
            children,
        )

        html_out = node.to_html()
        test_html = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"

        self.assertEqual(html_out, test_html)

    def test_parent_and_children(self):
        grand_children = [
            LeafNode("b", "Bold text"),
            LeafNode(None, "Normal text"),
            LeafNode("i", "italic text"),
            LeafNode("a", "Google", {"href": "https://www.google.com"}),
        ]
        children = [
            LeafNode("b", "Bold text"),
            ParentNode("div", grand_children),
            LeafNode("i", "italic text"),
            LeafNode(None, "Normal text"),
            LeafNode("a", "Google", {"href": "https://www.google.com"}),
        ]
        node = ParentNode("h1", children)
        self.assertEqual(node.tag, "h1")
        self.assertEqual(node.to_html(), '<h1><b>Bold text</b><div><b>Bold text</b>Normal text<i>italic text</i><a href="https://www.google.com">Google</a></div><i>italic text</i>Normal text<a href="https://www.google.com">Google</a></h1>')

# TODO: other test ideas??

if __name__ == "__main__":
    unittest.main()

