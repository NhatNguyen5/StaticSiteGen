import unittest
from logging_module.my_logging import log
from textnode import TextNode, TextType, text_node_to_html_node, split_nodes_delimiter


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
        self.longMessage = True
        cases = [
            (TextType.TEXT,   "This is a text node", None,     "This is a text node"),
            (TextType.BOLD,   "Bold Text",           "strong", "<strong>Bold Text</strong>"),
            (TextType.ITALIC, "Italic Text",         "em",     "<em>Italic Text</em>"),
            (TextType.CODE,   "Code Text",           "code",   "<code>Code Text</code>"),
        ]

        case_number = 0
        for text_type, text, tag, expected_html in cases:
            case_number += 1
            with self.subTest(text_type=text_type, msg=f"Case {case_number} failed"):
                node = TextNode(text, text_type)
                html_node = text_node_to_html_node(node)
                self.assertEqual(html_node.tag, tag)
                self.assertEqual(html_node.value, text)
                self.assertEqual(html_node.children, [])
                self.assertEqual(html_node.to_html(), expected_html)

    def test_text_node_to_html_node_all_void_types(self):
        self.longMessage = True
        cases = [
            (TextType.LINK,  "Link Text", "a", "https://example.com", '<a href="https://example.com">Link Text</a>'),
            (TextType.IMAGE, "Image Alt", "img", "https://example.com/image.png", '<img src="https://example.com/image.png" alt="Image Alt"/>'),
        ]

        case_number = 0
        for text_type, text, tag, url, expected_html in cases:
            with self.subTest(text_type=text_type, msg=f"Case {case_number} failed"):
                node = TextNode(text, text_type, url=url)
                html_node = text_node_to_html_node(node)
                self.assertEqual(html_node.tag, tag)
                if text_type == TextType.IMAGE:
                    self.assertEqual(html_node.value, "")
                else:
                    self.assertEqual(html_node.value, text)
                self.assertEqual(html_node.children, [])
                self.assertEqual(html_node.to_html(), expected_html)

    def test_split_nodes_delimiter_valid(self):
        old_nodes = [TextNode("This is a **bold** statement.", TextType.TEXT)]
        delimiter = "**"
        text_type = TextType.BOLD
        result = split_nodes_delimiter(old_nodes, delimiter, text_type)
        expected = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" statement.", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter_no_delimiter(self):
        old_nodes = [TextNode("No delimiter here.", TextType.TEXT)]
        delimiter = "**"
        text_type = TextType.BOLD
        with self.assertRaises(ValueError):
            split_nodes_delimiter(old_nodes, delimiter, text_type)

    def test_split_nodes_delimiter(self):
        self.longMessage = True
        old_nodes_cases = [
            # Text node containing delimiter                                              #delimiter #new text type
            [[TextNode("This is a **bold** statement.", TextType.TEXT)],                    "**",      TextType.BOLD],
            [[TextNode("No delimiter here.", TextType.TEXT)],                               "**",      TextType.BOLD],
            [[TextNode("**Starts with delimiter.", TextType.TEXT)],                         "**",      TextType.BOLD],
            [[TextNode("Ends with delimiter.**", TextType.TEXT)],                           "**",      TextType.BOLD],
            [[TextNode("Multiple **delimiters** in **one** line.", TextType.TEXT)],         "**",      TextType.BOLD],
            [                                                                             
                [                                                                         
                    TextNode("This is a **bold** statement.", TextType.TEXT),                           
                    TextNode("Multiple **delimiters** in **one** line.", TextType.TEXT),
                ],                                                                          "**", TextType.BOLD
            ],                                                                            
        ]
                                                                                          
        expected_nodes = [                                                                
            [                                                                             
                TextNode("This is a ", TextType.TEXT),                                    
                TextNode("bold", TextType.BOLD),                              
                TextNode(" statement.", TextType.TEXT)                        
            ],                                                                
                "Error",
                "Error",
                "Error",
            [
                TextNode("Multiple ", TextType.TEXT),
                TextNode("delimiters", TextType.BOLD),
                TextNode(" in ", TextType.TEXT),
                TextNode("one", TextType.BOLD),
                TextNode(" line.", TextType.TEXT)
            ],
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" statement.", TextType.TEXT),
                TextNode("Multiple ", TextType.TEXT),
                TextNode("delimiters", TextType.BOLD),
                TextNode(" in ", TextType.TEXT),
                TextNode("one", TextType.BOLD),
                TextNode(" line.", TextType.TEXT)
            ]
        ]

        case_number = 0
        for (old_nodes, delimiter, text_type), expected_node in zip(old_nodes_cases, expected_nodes):
            case_number += 1
            log(f"\nRunning case {case_number}")                          
            if expected_node == "Error":
                with self.assertRaises(ValueError, msg=f"Case {case_number} failed"):
                    split_nodes_delimiter(old_nodes, delimiter, text_type)
            else:
                new_nodes = split_nodes_delimiter(old_nodes, delimiter, text_type)
                self.assertEqual(new_nodes, expected_node, msg=f"Case {case_number} failed")

if __name__ == "__main__":
    unittest.main()