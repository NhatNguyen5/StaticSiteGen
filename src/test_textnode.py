import unittest
import sys
from logging_module.my_logging import logger
from textnode import TextNode
from utils import TextType, BlockType
from inline_markdown import text_node_to_html_node, split_nodes_delimiter, extract_markdown_images, extract_markdown_links, split_nodes_image, split_nodes_link, text_to_textnodes
from block_markdown import markdown_to_blocks, block_to_block_type


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
            (TextType.BOLD,   "Bold Text",           "b",      "<b>Bold Text</b>"),
            (TextType.ITALIC, "Italic Text",         "i",      "<i>Italic Text</i>"),
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
        skip_test = True
        if skip_test:
            return
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

        run_test(self, split_nodes_delimiter, old_nodes_cases, expected_nodes, log)

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

        run_test(self, extract_markdown_images, raw_texts, expected_results, log)

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

        run_test(self, extract_markdown_links, raw_texts, expected_results, log)

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

        run_test(self, split_nodes_image, old_nodes_cases, expected_results, log)

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

        run_test(self, split_nodes_link, old_nodes_cases, expected_results, log)

    def test_text_to_textnodes(self):
        skip_test = True
        if skip_test:
            return
        log = logger()
        log.enable = True
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
            [
                TextNode("This is incomplete text** with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            [
                TextNode("This is incomplete ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an _italic word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            [
                TextNode("This is incomplete ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a code block` and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
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
            [
                TextNode("This is incomplete text** with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" with trailing text", TextType.TEXT),
            ],
            [
                TextNode("This is incomplete ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an _italic word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
                TextNode(" with trailing text", TextType.TEXT),
            ],
            [
                TextNode("This is incomplete ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a code block` and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
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

        run_test(self, text_to_textnodes, raw_texts, expected_results, log)

    def test_markdown_to_blocks(self):
        skip_test = True
        if skip_test:
            return
        log = logger()
        log.enable = True
        md = [
"""
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
""",
        ]
        expected_results = [
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ]
        ]

        run_test(self, markdown_to_blocks, md, expected_results, log)

    def test_block_to_block_type(self):
        skip_test = True
        if skip_test:
            return
        log = logger()
        log.enable = True
        md = """
This is a paragraph.

# This is a heading.

#### This is also a heading.

#### This is also a heading.
```
This is a code block
With 2 lines
```

#,# This is not a heading.

####### This not a heading.

```This is a code block```

```
This is a code block
With 2 lines
```

```This is not a code block

This is not a code block```

#### This is also a heading.```

>This is a quote block line 1
>This is a quote block line 2
>This is a quote block line 3
>#### This is a quote block line 4```

>This is not a quote block line 1
This is not a quote block line 2
>This is not a quote block line 3

>This is a quote block line 1
> 
>This is a quote block line 3

- This is an unordered list
- with items
- another items
- #### This is still an item```

- This is not an unordered list
 with items
- another items

1. This is an ordered list
2. with items
3. another items
4. #### This is still an item```

1. This is not an ordered list
2. 
3. another items

1. This is not an ordered list
with items
3. another items

2. This is not an ordered list
3. with items
4. another items
            """
        blocks = markdown_to_blocks(md)

        expected_results = [
            BlockType.PARAGRAPH,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.HEADING,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.CODE,
            BlockType.CODE,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.HEADING,
            BlockType.QUOTE,
            BlockType.PARAGRAPH,
            BlockType.QUOTE,
            BlockType.UNORDEREDLIST,
            BlockType.PARAGRAPH,
            BlockType.ORDEREDLIST,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
            BlockType.PARAGRAPH,
        ]

        run_test(self, block_to_block_type, blocks, expected_results, log)

def run_test(unit_test, test_function, test_cases, expected_results, log):
    log("==============================================")
    log(f"Test for: {sys._getframe(1).f_code.co_name}")
    case_number = 0
    for case, expected_result in zip(test_cases, expected_results):
        case_number += 1
        log(f"\nRunning case {case_number}")

        # unpack tuple
        def unpack():
            if isinstance(case, (tuple, list)):
                return test_function(*case)
            if isinstance(case, dict):
                return test_function(**case)
            return test_function(case)
        
        if expected_result == "Error":
            with unit_test.assertRaises(ValueError, msg=f"Case {case_number} failed") as e:
                unpack()
            log(f"Expected error: {e.exception}")
        else:
            result = unpack()
            unit_test.assertEqual(result, expected_result, msg=f"Case {case_number} failed")

if __name__ == "__main__":
    unittest.main()