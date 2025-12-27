from enum import Enum

class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class TextNode:
    def __init__(self, text: str, text_type: TextType = TextType.TEXT, url: str = None):
        self.text = text
        self.text_type = text_type
        self.url = url  # Used for links and images

    def __eq__(self, other):
        return isinstance(other, TextNode) and self.text == other.text and self.text_type == other.text_type and self.url == other.url

    def __repr__(self):
        return f"TextNode({self.text}, {self.text_type}, {self.url})"

    def render(self) -> str:
        if self.text_type == TextType.BOLD:
            return f"<strong>{self.text}</strong>"
        elif self.text_type == TextType.ITALIC:
            return f"<em>{self.text}</em>"
        elif self.text_type == TextType.CODE:
            return f"<code>{self.text}</code>"
        elif self.text_type == TextType.LINK:
            return f'<a href="{self.href}">{self.text}</a>'
        elif self.text_type == TextType.IMAGE:
            return f'<img src="{self.href}" alt="{self.alt_text}" />'
        else:
            return self.text