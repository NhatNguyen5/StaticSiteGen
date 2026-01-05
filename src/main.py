import os
import shutil
import sys
from build import copyDir
from gen_content import generate_pages_recursive

def main():
    first_arg = sys.argv[0]
    basepath = "/" if not first_arg else first_arg
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    os.mkdir("docs")
    copyDir("static", "docs")

    #generate_page("content/index.md", "template.html")
    generate_pages_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()