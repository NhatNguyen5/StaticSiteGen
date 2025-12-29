import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode("div", "Hello World", [], {})
        node2 = HTMLNode("div", "Hello World", [], {})
        self.assertEqual(node, node2)

    def test_neq(self):
        node = HTMLNode("div", "Hello World", [], {})
        node2 = HTMLNode("p", "Hello World", [], {})
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = HTMLNode("div", "Hello World", [], {"class": "container"})
        self.assertEqual(repr(node), "HTMLNode(tag=div, props={'class': 'container'}, children=[])")

    def test_props_to_html(self):
        node = HTMLNode("a", "Click here", [], {"href": "https://example.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), 'href="https://example.com" target="_blank"')

    def test_to_html_not_implemented(self):
        node = HTMLNode("div")
        with self.assertRaises(NotImplementedError):
            node.to_html()

class TestLeafNode(unittest.TestCase):
    def test_leafnode_to_html_p(self):
        leaf = LeafNode("p", "This is a paragraph.")
        self.assertEqual(leaf.to_html(), '<p>This is a paragraph.</p>')
    
    def test_leafnode_to_html_no_tag(self):
        leaf = LeafNode(None, "Just some text.")
        self.assertEqual(leaf.to_html(), 'Just some text.')

    def test_leafnode_to_html_no_value(self):
        leaf = LeafNode("p", None)
        with self.assertRaises(ValueError):
            leaf.to_html()

    def test_leafnode_to_html_with_props(self):
        leaf = LeafNode("a", "Link", {"href": "https://example.com"})
        self.assertEqual(leaf.to_html(), '<a href="https://example.com">Link</a>')

class TestParentNode(unittest.TestCase):
    def test_parentnode_to_html_div(self):
        child1 = LeafNode("p", "Paragraph 1")
        child2 = LeafNode("p", "Paragraph 2")
        parent = ParentNode("div", [child1, child2])
        self.assertEqual(parent.to_html(), '<div><p>Paragraph 1</p><p>Paragraph 2</p></div>')

    def test_parentnode_to_html_no_tag(self):
        child = LeafNode("p", "Paragraph")
        parent = ParentNode(None, [child])
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_parentnode_to_html_no_props(self):
        child = LeafNode("p", "Content")
        parent = ParentNode("section", [child])
        self.assertEqual(parent.to_html(), '<section><p>Content</p></section>')

    def test_parentnode_to_html_with_props(self):
        child = LeafNode("p", "Content")
        parent = ParentNode("section", [child], {"class": "main-section"})
        self.assertEqual(parent.to_html(), '<section class="main-section"><p>Content</p></section>')

    def test_parentnode_to_html_no_children(self):
        parent = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent.to_html()

    def test_parentnode_to_html_empty_children(self):
        parent = ParentNode("div", [])
        self.assertEqual(parent.to_html(), "<div></div>")

    def test_parentnode_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_parentnode_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

if __name__ == "__main__":
    unittest.main()