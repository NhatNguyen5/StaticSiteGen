import unittest
import inspect
import sys
from logging_module.my_logging import logger
from textnode import TextNode, TextType
from inline_markdown import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes

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
        result = split_nodes_delimiter(old_nodes, delimiter, text_type)
        expected = [
            TextNode("No delimiter here.", TextType.TEXT)
        ]
        self.assertEqual(result, expected)

    def test_split_nodes_delimiter(self):
        log = logger()
        log.enable = False
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
            [
                TextNode("No delimiter here.", TextType.TEXT),
            ],
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

    def test_extract_markdown_images(self):
        skip_test = True
        if skip_test:
            return
        log = logger()
        log.enable = False
        self.longMessage = True
        raw_texts = [
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
        ]

        expected_results = [
            [("image", "https://i.imgur.com/zjjcJKZ.png")]
        ]

        case_number = 0
        for text, expected_result in zip(raw_texts, expected_results):
            case_number += 1
            log(f"\nRunning case {case_number}")                          
            if expected_result == "Error":
                with self.assertRaises(ValueError, msg=f"Case {case_number} failed"):
                    match = extract_markdown_images(text)
            else:
                match = extract_markdown_images(text)
                self.assertEqual(match, expected_result, msg=f"Case {case_number} failed")

    def test_extract_markdown_links(self):
        skip_test = True
        if skip_test:
            return
        log = logger()
        log.enable = False
        self.longMessage = True
        raw_texts = [
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
        ]

        expected_results = [
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev")
            ]
        ]

        case_number = 0
        for text, expected_result in zip(raw_texts, expected_results):
            case_number += 1
            log(f"\nRunning case {case_number}")                          
            if expected_result == "Error":
                with self.assertRaises(ValueError, msg=f"Case {case_number} failed"):
                    match = extract_markdown_links(text)
            else:
                match = extract_markdown_links(text)
                self.assertEqual(match, expected_result, msg=f"Case {case_number} failed")

    def test_split_node_image(self):
        skip_test = True
        if skip_test:
            return
        log = logger()
        log.enable = True
        self.longMessage = True
        old_nodes_cases = [
            [
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
            ],
            [
                TextNode("Nothing to extract", TextType.TEXT),
            ],
            [
                TextNode("This is text with an image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
            ],
            [
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) with trailing text", TextType.TEXT),
            ],
            [
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)", TextType.TEXT),
                TextNode("This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png) with trailing text", TextType.TEXT),
            ]
        ]

        expected_results = [
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            [
                TextNode("Nothing to extract", TextType.TEXT),
            ],
            [
                TextNode("This is text with an image](https://i.imgur.com/zjjcJKZ.png) and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
            ],
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" with trailing text", TextType.TEXT),
            ],
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode("second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"),
                TextNode(" with trailing text", TextType.TEXT),
            ],
        ]

        case_number = 0
        for old_nodes, expected_result in zip(old_nodes_cases, expected_results):
            case_number += 1
            log(f"\nRunning case {case_number}")                          
            if expected_result == "Error":
                with self.assertRaises(ValueError, msg=f"Case {case_number} failed"):
                    match = split_nodes_image(old_nodes)
            else:
                match = split_nodes_image(old_nodes)
                self.assertEqual(match, expected_result, msg=f"Case {case_number} failed")

    def test_split_node_link(self):
        skip_test = True
        if skip_test:
            return
        log = logger()
        log.enable = False
        self.longMessage = True
        old_nodes_cases = [
            [
                TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT),
            ],
            [
                TextNode("Nothing to extract", TextType.TEXT),
            ],
            [
                TextNode("This is text with a link [to boot dev](https://www.boot.dev) and to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT),
            ],
            [
                TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) with trailing text", TextType.TEXT),
            ],
            [
                TextNode("This is text with a link [to boot dev](https://www.boot.dev) and to youtube](https://www.youtube.com/@bootdotdev) with trailing text", TextType.TEXT),
            ],
            [
                TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT),
                TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) with trailing text", TextType.TEXT),
            ]
        ]

        expected_results = [
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ],
            [
                TextNode("Nothing to extract", TextType.TEXT),
            ],
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT),
            ],
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode(" with trailing text", TextType.TEXT),
            ],
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and to youtube](https://www.youtube.com/@bootdotdev)  with trailing text", TextType.TEXT),
            ],
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode(" with trailing text", TextType.TEXT),
            ],
        ]

        case_number = 0
        for old_nodes, expected_result in zip(old_nodes_cases, expected_results):
            case_number += 1
            log(f"\nRunning case {case_number}")                          
            if expected_result == "Error":
                with self.assertRaises(ValueError, msg=f"Case {case_number} failed"):
                    match = split_nodes_link(old_nodes)
            else:
                match = split_nodes_link(old_nodes)
                self.assertEqual(match, expected_result, msg=f"Case {case_number} failed")

    def test_split_node_link(self):
        skip_test = False
        if skip_test:
            return
        log = logger()
        log.enable = True
        log("==============================================")
        log(f"Logging for: {sys._getframe().f_code.co_name}")
        self.longMessage = True
        raw_texts = [
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
            "This is incomplete text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
            "This is incomplete **text** with an _italic word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
            "This is incomplete **text** with an _italic_ word and a code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
            "This is incomplete **text** with an _italic_ word and a `code block` and an obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)",
            "This is incomplete **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a link](https://boot.dev)",
            "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) with trailing text",
            "This is incomplete text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) with trailing text",
            "This is incomplete **text** with an _italic word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) with trailing text",
            "This is incomplete **text** with an _italic_ word and a code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) with trailing text",
            "This is incomplete **text** with an _italic_ word and a `code block` and an obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev) with trailing text",
            "This is incomplete **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a link](https://boot.dev) with trailing text",
        ]

        expected_results = [
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            "Error",
            "Error",
            "Error",
            [
                TextNode("This is incomplete ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            [
                TextNode("This is incomplete ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a link](https://boot.dev)", TextType.TEXT),
            ],
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" with trailing text", TextType.TEXT),
            ],
            "Error",
            "Error",
            "Error",
            [
                TextNode("This is incomplete ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" with trailing text", TextType.TEXT),
            ],
            [
                TextNode("This is incomplete ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a link](https://boot.dev) with trailing text", TextType.TEXT),
            ],
        ]

        case_number = 0
        for text, expected_result in zip(raw_texts, expected_results):
            case_number += 1
            log(f"\nRunning case {case_number}")                          
            if expected_result == "Error":
                with self.assertRaises(ValueError, msg=f"Case {case_number} failed") as e:
                    match = text_to_textnodes(text)
                log(f"Expected error: {e.exception}")
            else:
                match = text_to_textnodes(text)
                self.assertEqual(match, expected_result, msg=f"Case {case_number} failed")

if __name__ == "__main__":
    unittest.main()