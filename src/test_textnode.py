import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_neq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("Sample", TextType.ITALIC)
        self.assertEqual(repr(node), "TextNode(Sample, TextType.ITALIC, None)")

    def test_render_bold(self):
        node = TextNode("Bold Text", TextType.BOLD)
        self.assertEqual(node.render(), "<strong>Bold Text</strong>")

    def test_render_italic(self):
        node = TextNode("Italic Text", TextType.ITALIC)
        self.assertEqual(node.render(), "<em>Italic Text</em>")

    def test_render_code(self):
        node = TextNode("Code Text", TextType.CODE)
        self.assertEqual(node.render(), "<code>Code Text</code>")

if __name__ == "__main__":
    unittest.main()