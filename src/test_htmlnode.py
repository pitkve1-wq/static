import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("This", "1", "none")
        node2 = HTMLNode("This", "1", "none")
        self.assertEqual(node.tag, node2.tag)
        self.assertEqual(node.value, node2.value)

    def test_wq(self):
        node = HTMLNode(
            "This", "1", "none", {"href": "https://www.google.com", "target": "_blank"}
        )
        node2 = HTMLNode(
            "This", "1", "node", {"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(node.tag, node2.tag)
        self.assertEqual(node.value, node2.value)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")
        node = LeafNode("p", "Hello, world!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(), '<p href="https://www.google.com">Hello, world!</p>'
        )

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )
