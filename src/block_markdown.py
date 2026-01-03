from logging_module.my_logging import logger
from utils import BlockType


def markdown_to_blocks(markdown):
    log = logger()
    log.enable = True
    log("==============================================")
    lines = [line.strip() for line in markdown.split("\n\n")]
    lines = [line for line in lines if line]
    log(f"Lines: {lines}")
    return lines

def block_to_block_type(block):
    pass