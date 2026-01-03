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
        if node.text_type != TextType.TEXT or node.text.count(delimiter)==0:
            if node.text_type != TextType.TEXT:
                log(f"Skipping node as its type is not TEXT: {node.text_type}")
            elif node.text.count(delimiter)==0:
                log(f"Skipping node as no delimiter found: {delimiter}")    
            new_nodes.append(node)
        else:                                     
            if node.text.count(delimiter)%2==1:
                log(f"Error processing: Invalid Markdown structure: Delimiter {delimiter} not in pair in text node.")
                raise ValueError(f"Invalid Markdown structure: Delimiter {delimiter} not in pair in text node.")
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
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    log(f"Matches: {matches}")
    return matches

def extract_markdown_links(text):
    log = logger()
    log.enable = False
    log("==============================================")
    log(text)
    matches = re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    log(f"Matches: {matches}")
    return matches

def split_nodes_image(old_nodes):
    new_nodes = []
    log = logger()
    log.enable = False
    log("==============================================")
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            log(f"Skipping node as its type is not TEXT: {node.text_type}")
            new_nodes.append(node)
            continue
        log(f"Processing node: {node}")
        extracted_data = extract_markdown_images(node.text)
        if not extracted_data:
            log(f"Skipping node as there's nothing to extract: {node.text_type}")
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for alt_text, img_link in extracted_data:
            log(f"Extracted data: {alt_text}, {img_link}")
            text_section = remaining_text.split(f"![{alt_text}]({img_link})", 2)
            new_nodes.append(TextNode(text_section[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.IMAGE, img_link))
            log(f"Split text: {text_section}")
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
        if node.text_type != TextType.TEXT:
            log(f"Skipping node as its type is not TEXT: {node.text_type}")
            new_nodes.append(node)
            continue
        log(f"Processing node: {node}")
        extracted_data = extract_markdown_links(node.text)
        if not extracted_data:
            log(f"Skipping node as there's nothing to extract: {node.text_type}")
            new_nodes.append(node)
            continue
        remaining_text = node.text
        for alt_text, link in extracted_data:
            log(f"{alt_text}, {link}")
            text_section = remaining_text.split(f"[{alt_text}]({link})", 2)
            new_nodes.append(TextNode(text_section[0], TextType.TEXT))
            new_nodes.append(TextNode(alt_text, TextType.LINK, link))
            log(f"new_node: {new_nodes}")
            log(f"Split text: {text_section}")
            remaining_text = text_section[1]
            log(remaining_text)
        if remaining_text != "":
            new_nodes.append(TextNode(remaining_text, TextType.TEXT))
    return new_nodes

def text_to_textnodes(text):
    log = logger()
    log.enable = False
    log("\n==============================================")
    nodes = [TextNode(text, TextType.TEXT)]
    log(f"Before BOLD: {nodes}")
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    log(f"After BOLD: {nodes}")
    log(f"Before ITALIC: {nodes}")
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    log(f"After ITALIC: {nodes}")
    log(f"Before CODE: {nodes}")
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    log(f"After CODE: {nodes}")
    log(f"Before IMAGE: {nodes}")
    nodes = split_nodes_image(nodes)
    log(f"After IMAGE: {nodes}")
    log(f"Before LINK: {nodes}")
    nodes = split_nodes_link(nodes)
    log(f"After LINK: {nodes}")
    return nodes