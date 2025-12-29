from htmlnode import LeafNode
from utils import TextType


class TextNode:
    def __init__(self, text: str, text_type: TextType = TextType.TEXT, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url  # Used for links and images

    def __eq__(self, other):
        return (
            isinstance(other, TextNode) and 
            self.text == other.text and 
            self.text_type == other.text_type and 
            self.url == other.url
        )

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        return LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        return LeafNode("strong", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        return LeafNode("em", text_node.text)
    elif text_node.text_type == TextType.CODE:
        return LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        return LeafNode("a", text_node.text, props={"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        return LeafNode("img", "", props={"src": text_node.url, "alt": text_node.text})
    else:
        raise ValueError("Unsupported TextType for rendering to HTML.")