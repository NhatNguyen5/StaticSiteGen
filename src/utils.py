from enum import Enum


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDEREDLIST = "unordered_list"
    ORDEREDLIST = "ordered_list"

class VoidTags(Enum):
    IMG = "img"
    BR = "br"
    HR = "hr"
    INPUT = "input"
    META = "meta"
    LINK = "link"
    AREA = "area"
    BASE = "base"
    COL = "col"
    EMBED = "embed"
    PARAM = "param"
    SOURCE = "source"
    TRACK = "track"
    WBR = "wbr"