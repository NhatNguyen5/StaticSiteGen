import unittest
import sys
from htmlnode import HTMLNode, LeafNode, ParentNode
from block_markdown import markdown_to_html_node
from logging_module.my_logging import logger


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

class TestMarkdownToHTML(unittest.TestCase):
    def test_markdown_to_html_node(self):
        skip_test = False
        if skip_test:
            return
        log = logger()
        log.enable = True
        log("==============================================")
        func_name = sys._getframe().f_code.co_name
        log(f"Test for: {func_name}")
        mds = [
"""
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

""",
"""
```
This is text that _should_ remain
the **same** even with inline stuff
```
""",
"""- item one
- item two
""",
"""- first **bold**
- second with `code`
""",
"""- item one
-   
- item three
""",
"""1. first
2. second
3. third
""",
"""
1. first
2. second
3. third
4. first
5. second
6. third
7. first
8. second
9. nine
10. ten
11. eleven
""",
"""- one
- two

Regular paragraph
""",
"""
# This is a heading.

#### This is also a heading.

#,# This is not a heading.

####### This not a heading.

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
"""
        ]
        
        expected_results = [
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
            "<div><ul><li>item one</li><li>item two</li></ul></div>",
            "<div><ul><li>first <b>bold</b></li><li>second with <code>code</code></li></ul></div>",
            "<div><p>- item one - - item three</p></div>",
            "<div><ol><li>first</li><li>second</li><li>third</li></ol></div>",
            "<div><ol><li>first</li><li>second</li><li>third</li><li>first</li><li>second</li><li>third</li><li>first</li><li>second</li><li>nine</li><li>ten</li><li>eleven</li></ol></div>",
            "<div><ul><li>one</li><li>two</li></ul><p>Regular paragraph</p></div>",
            "<div><h1>This is a heading.</h1><h4>This is also a heading.</h4><p>#,# This is not a heading.</p><p>####### This not a heading.</p><pre><code>This is a code block\nWith 2 lines\n</code></pre><p>```This is not a code block</p><p>This is not a code block```</p><h4>This is also a heading.```</h4><blockquote>This is a quote block line 1\nThis is a quote block line 2\nThis is a quote block line 3\n#### This is a quote block line 4```</blockquote><p>>This is not a quote block line 1 This is not a quote block line 2 >This is not a quote block line 3</p><blockquote>This is a quote block line 1\n\nThis is a quote block line 3</blockquote><ul><li>This is an unordered list</li><li>with items</li><li>another items</li><li>#### This is still an item```</li></ul></div>"
        ]

        case_number = 0
        for md, expected_result in zip(mds, expected_results):
            case_number += 1
            log(f"\nRunning case {case_number}")
            node = markdown_to_html_node(md)
            html = node.to_html()
            self.assertEqual(html, expected_result, msg=f"Case {case_number} failed")
            log(f"\nCase {case_number} passed!")

if __name__ == "__main__":
    unittest.main()