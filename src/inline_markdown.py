from htmlnode import LeafNode
import re
from utils import TextType
from textnode import TextNode
from logging_module.my_logging import logger

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
    log.enable = False
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

def split_nodes_image(old_nodes):
    new_nodes = []
    log = logger()
    log.enable = False
    log("==============================================")
    for node in old_nodes:
        log(f"Processing node: {node}")
        extracted_data = extract_markdown_images(node.text)
        remaining_text = node.text
        for alt_text, img_link in extracted_data:
            log(f"{alt_text}, {img_link}")
            text_section = remaining_text.split(f"![{alt_text}]({img_link})", 2)
            new_nodes.append(TextNode(text_section[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, img_link))
            remaining_text = text_section[1]
            log(remaining_text)
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    log = logger()
    log.enable = False
    log("==============================================")
    for node in old_nodes:
        log(f"Processing node: {node}")
        extracted_data = extract_markdown_links(node.text)
        remaining_text = node.text
        for alt_text, link in extracted_data:
            log(f"{alt_text}, {link}")
            text_section = remaining_text.split(f"[{alt_text}]({link})", 2)
            new_nodes.append(TextNode(text_section[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.LINK, link))
            remaining_text = text_section[1]
            log(remaining_text)
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    pass