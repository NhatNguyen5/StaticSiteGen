import os, sys
from logging_module.my_logging import logger
from block_markdown import markdown_to_html_node

def generate_page(from_path, template_path, dest_path):
    log = logger()
    log.enable = True
    log("==============================================")
    func_name = sys._getframe().f_code.co_name
    log(f"Log for: {func_name}")
    log(f"Generating page from {from_path} to {dest_path} using {template_path}", True)
    markdown = ""
    with open(from_path, 'r', encoding='utf-8') as f:
        markdown = f.read()
    template = ""
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    title = extract_title(markdown)
    markdown_to_html = markdown_to_html_node(markdown).to_html()

    log(markdown_to_html)

    full_html = template.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", markdown_to_html)

    log(full_html)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(full_html)

def extract_title(markdown):
    log = logger()
    log.enable = False
    log("==============================================")
    func_name = sys._getframe().f_code.co_name
    log(f"Log for: {func_name}")
    first_line = markdown.strip().split("\n",1)[0]
    log(f"Processing: {markdown}")
    log(f"First line: {first_line}")
    if first_line.startswith("# ") and first_line[2:].strip() != "":
        return first_line[2:]
    else:
        raise ValueError("No header!")