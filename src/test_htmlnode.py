import unittest

from htmlnode import HTMLNode


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

if __name__ == "__main__":
    unittest.main()