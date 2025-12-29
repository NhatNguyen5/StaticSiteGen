import unittest
from textnode import TextNode, TextType, text_node_to_html_node


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

    def test_text_node_to_html_node_all_non_void_types(self):
        cases = [
            (TextType.TEXT,   "This is a text node", None,     "This is a text node"),
            (TextType.BOLD,   "Bold Text",           "strong", "<strong>Bold Text</strong>"),
            (TextType.ITALIC, "Italic Text",         "em",     "<em>Italic Text</em>"),
            (TextType.CODE,   "Code Text",           "code",   "<code>Code Text</code>"),
        ]

        for text_type, text, tag, expected_html in cases:
            with self.subTest(text_type=text_type):
                node = TextNode(text, text_type)
                html_node = text_node_to_html_node(node)
                self.assertEqual(html_node.tag, tag)
                self.assertEqual(html_node.value, text)
                self.assertEqual(html_node.children, [])
                self.assertEqual(html_node.to_html(), expected_html)

    def test_text_node_to_html_node_all_void_types(self):
        cases = [
            (TextType.LINK,  "Link Text", "a", "https://example.com", '<a href="https://example.com">Link Text</a>'),
            (TextType.IMAGE, "Image Alt", "img", "https://example.com/image.png", '<img src="https://example.com/image.png" alt="Image Alt"/>'),
        ]

        for text_type, text, tag, url, expected_html in cases:
            with self.subTest(text_type=text_type):
                node = TextNode(text, text_type, url=url)
                html_node = text_node_to_html_node(node)
                self.assertEqual(html_node.tag, tag)
                if text_type == TextType.IMAGE:
                    self.assertEqual(html_node.value, "")
                else:
                    self.assertEqual(html_node.value, text)
                self.assertEqual(html_node.children, [])
                self.assertEqual(html_node.to_html(), expected_html)

if __name__ == "__main__":
    unittest.main()