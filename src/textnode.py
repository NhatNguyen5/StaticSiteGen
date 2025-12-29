from htmlnode import LeafNode
from utils import TextType
import re
from logging_module.my_logging import logger


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
                                                  
def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    log = logger()
    log.enable = False
    log("==============================================")
    for node in old_nodes:
        log(f"Processing node: {node}")                        
        if node.text_type != TextType.TEXT:
            log(f"Skipping node as its type is not TEXT: {node.text_type}")       
            new_nodes.append(node)                
        else:                                     
            if node.text.count(delimiter) < 2:    
                raise ValueError("Invalid Markdown structure: Delimiter not found in text node.")
            parts = node.text.split(delimiter) 
            log(f"Splitting node '{node.text}' into parts: {parts}")
            for i, part in enumerate(parts): 
                log(f"Processing part {i}: '{part}'")                              
                new_nodes.append(TextNode(part, text_type if i % 2 == 1 else TextType.TEXT, node.url))  
            log(f"Resulting nodes after split: {new_nodes}")                       
    return new_nodes

def extract_markdown_images(text):
    log = logger()
    log.enable = False
    log("==============================================")
    log(text)
    ret_extracted = []
    alt_texts = re.findall(r"\!\[(.*?)\]", text)
    log(f"{alt_texts}")
    link_texts = re.findall(r"\((https://.*?)\)",text)
    log(f"{link_texts}")
    for alt_text, link_text in zip(alt_texts, link_texts):
        ret_extracted.append((alt_text, link_text))
        log(f"{ret_extracted}")
    return ret_extracted

def extract_markdown_links(text):
    log = logger()
    log.enable = True
    log("==============================================")
    log(text)
    ret_extracted = []
    alt_texts = re.findall(r"\[(.*?)\]", text)
    log(f"{alt_texts}")
    link_texts = re.findall(r"\((https://.*?)\)",text)
    log(f"{link_texts}")
    for alt_text, link_text in zip(alt_texts, link_texts):
        ret_extracted.append((alt_text, link_text))
        log(f"{ret_extracted}")
    return ret_extracted
