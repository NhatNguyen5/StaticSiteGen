import os, sys
from logging_module.my_logging import logger
from block_markdown import markdown_to_html_node
from inline_markdown import extract_title

def generate_page(from_path, template_path, dest_path, basepath):
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

    #log(markdown_to_html)
    log(f"basepath: {basepath}")
    full_html = template.replace("{{ Title }}", title)
    full_html = full_html.replace("{{ Content }}", markdown_to_html)
    full_html = full_html.replace("href=\"/", f"href=\"{basepath}")
    full_html = full_html.replace("src=\"/", f"src=\"{basepath}")

    #log(full_html)

    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w") as f:
        f.write(full_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    log = logger()
    log.enable = True
    log("==============================================")
    func_name = sys._getframe().f_code.co_name
    log(f"Log for: {func_name}")
    all_objects = os.listdir(dir_path_content)
    for object in all_objects:
        src_path = os.path.join(dir_path_content, object)
        log(f"Object: {object}")
        if os.path.isfile(src_path) and object.endswith(".md"):
            file_name = object.rsplit(".", 1)[0] + ".html"
            dest_path = os.path.join(dest_dir_path, file_name)          
            log(f"Generate file: from {src_path} to {dest_path}")
            generate_page(src_path, template_path, dest_path, basepath)
            continue
        new_dest_path = os.path.join(dest_dir_path, object)
        os.mkdir(new_dest_path)
        log(f"Generate dir: from {src_path} to {new_dest_path}")
        generate_pages_recursive(src_path, template_path, new_dest_path, basepath)
    return 0