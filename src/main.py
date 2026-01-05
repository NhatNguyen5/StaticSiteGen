import os
import shutil
import sys
from logging_module.my_logging import logger
from build import copyDir
from gen_content import generate_pages_recursive

def main():
    log = logger()
    log.enable = True
    log("==============================================")
    func_name = sys._getframe().f_code.co_name
    log(f"Log for: {func_name}")
    log(f"argv: {sys.argv}")
    first_argv = sys.argv[1]
    basepath = "/" if not first_argv else first_argv
    if os.path.exists("docs"):
        shutil.rmtree("docs")
    os.mkdir("docs")
    copyDir("static", "docs")

    #generate_page("content/index.md", "template.html")
    generate_pages_recursive("content", "template.html", "docs", basepath)

if __name__ == "__main__":
    main()