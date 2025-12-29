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

    def test_text_node_to_html_nodetext(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
        self.assertEqual(html_node.props, {})
        self.assertEqual(html_node.children, [])
        self.assertEqual(html_node.to_html(), "This is a text node")

    def test_text_node_to_html_node_bold(self):
        node = TextNode("Bold Text", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "strong")
        self.assertEqual(html_node.value, "Bold Text")
        self.assertEqual(html_node.props, {})
        self.assertEqual(html_node.children, [])
        self.assertEqual(html_node.to_html(), "<strong>Bold Text</strong>")

    def test_text_node_to_html_node_italic(self):
        node = TextNode("Italic Text", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<em>Italic Text</em>")

    def test_text_node_to_html_node_code(self):
        node = TextNode("Code Text", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<code>Code Text</code>")
        
    def test_text_node_to_html_node_link(self):
        node = TextNode("Link Text", TextType.LINK, url="https://example.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<a href="https://example.com">Link Text</a>')

    def test_text_node_to_html_node_image(self):
        node = TextNode("Image Alt", TextType.IMAGE, url="https://example.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<img src="https://example.com/image.png" alt="Image Alt"/>')

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