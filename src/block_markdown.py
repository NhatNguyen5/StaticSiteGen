from logging_module.my_logging import logger
from utils import TextType, BlockType
from htmlnode import ParentNode
from textnode import TextNode
from inline_markdown import text_to_textnodes, text_node_to_html_node


def markdown_to_blocks(markdown):
    log = logger()
    log.enable = False
    log("==============================================")
    lines = [line.strip() for line in markdown.split("\n\n")]
    lines = [line for line in lines if line]
    log(f"Lines: {lines}")
    return lines

def block_to_block_type(block):
    log = logger()
    log.enable = False
    log("\n==============================================")
    log(f"Processing:\n{block}")
    block_type = BlockType.PARAGRAPH
    if isCodeBlock(block):
        block_type = BlockType.CODE
    elif isHeadings(block):
        block_type = BlockType.HEADING
    elif isQuoteBlock(block):
        block_type = BlockType.QUOTE
    elif isUnorderedList(block):
        block_type = BlockType.UNORDEREDLIST
    elif isOrderedList(block):
        block_type = BlockType.ORDEREDLIST
    log(f"block_type: {block_type}")
    return block_type

def isCodeBlock(block):
    return block[:3] == "```" and block[-3:] == "```"

def isHeadings(block):
    starting_chars = block.split(" ", 1)[0]
    return set(starting_chars) == {'#'} and 1 <= len(starting_chars) <= 6

def isQuoteBlock(block):
    lines = block.split('\n')
    return all(line[0] == ">" for line in lines)

def isUnorderedList(block):
    lines = block.split('\n')
    return all(line.startswith("- ") and line[2:].strip() for line in lines)

def isOrderedList(block):
    lines = block.split('\n')
    return all(line.startswith(f"{i+1}. ") and line[len(f"{i+1}. "):].strip() for i, line in enumerate(lines))

def markdown_to_html_node(markdown):
    log = logger()
    log.enable = False
    log("\n==============================================")
    blocks = markdown_to_blocks(markdown)
    children_nodes = []
    for block in blocks:
        log(f"Processing:\n{block}")
        block_type = block_to_block_type(block)
        child_node = ""
        if block_type == BlockType.CODE:
            child_node = processCodeBlock(block)
        elif block_type == BlockType.HEADING:
            child_node = processHeadingBlock(block)
        elif block_type == BlockType.QUOTE:
            child_node = processQuoteBlock(block)
        elif block_type == BlockType.UNORDEREDLIST:
            child_node = processUnorderedList(block)
        elif block_type == BlockType.ORDEREDLIST:
            child_node = processOrderedList(block)
        else:
            child_node = processParagraph(block)
        log(f"Processed node: {child_node}")
        children_nodes.append(child_node)
    div_node = ParentNode("div", children_nodes)
    log(f"Result: {div_node.to_html()}")
    return div_node

def processCodeBlock(block):
    block_text = "\n".join(block.split("\n")[1:-1])+"\n"
    code_leaf = text_node_to_html_node(TextNode(block_text, TextType.TEXT))
    return ParentNode("pre",[ParentNode("code",[code_leaf])])

def processHeadingBlock(block):
    heading_marks, text_part = block.split(" ", 1)
    heading_level = len(heading_marks)
    return ParentNode(f"h{heading_level}", toGrandChildren(text_part))

def processQuoteBlock(block):
    clean_lines = []
    lines = block.split("\n")
    for line in lines:
        if line == "":
            clean_lines.append("")
            continue
        if len(line) > 1 and line[1] == " ":
            clean_line = line[2:]   # drop "> "
        else:
            clean_line = line[1:]   # drop ">"
        clean_lines.append(clean_line)
    text_part = "\n".join(clean_lines)
    return ParentNode("blockquote", toGrandChildren(text_part))

def processUnorderedList(block):
    leaf_nodes = []
    lines = block.split("\n")
    for line in lines:
        clean_line = line[2:]   # drop "- "
        text_nodes = text_to_textnodes(clean_line)
        list_items = [text_node_to_html_node(text_node) for text_node in text_nodes]
        leaf_nodes.append(ParentNode("li", list_items))
    return ParentNode("ul", leaf_nodes)
    

def processOrderedList(block):
    leaf_nodes = []
    lines = block.split("\n")
    i = 1
    for line in lines:
        clean_line = line[len(f"{i}. "):]   # drop "x. "
        text_nodes = text_to_textnodes(clean_line)
        list_items = [text_node_to_html_node(text_node) for text_node in text_nodes]
        leaf_nodes.append(ParentNode("li", list_items))
        i+=1
    return ParentNode("ol", leaf_nodes)

def processParagraph(block):
    text_part = " ".join(line.strip() for line in block.split("\n")).strip()
    return ParentNode("p",toGrandChildren(text_part))

def toGrandChildren(block):
    log = logger()
    log.enable = False
    grand_children_nodes = []
    text_nodes = text_to_textnodes(block)
    for node in text_nodes:
        log(f"  Processing node: {node}")
        grand_children_nodes.append(text_node_to_html_node(node))
    return grand_children_nodes