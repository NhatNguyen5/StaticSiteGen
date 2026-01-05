import os
import shutil
from logging_module.my_logging import logger
from build import copyDir
from gen_content import generate_pages_recursive

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    copyDir("static", "public")

    #generate_page("content/index.md", "template.html")
    generate_pages_recursive("content", "template.html", "public")

if __name__ == "__main__":
    main()