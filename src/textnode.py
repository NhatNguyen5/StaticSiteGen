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