import os
import shutil
from logging_module.my_logging import logger
from build import copyDir
from gen_content import generate_page

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    copyDir("static", "public")

    generate_page("content/index.md", "template.html", "public/index.html")

if __name__ == "__main__":
    main()