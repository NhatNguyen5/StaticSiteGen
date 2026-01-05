import os
import shutil
from logging_module.my_logging import logger

def main():
    if os.path.exists("public"):
        shutil.rmtree("public")
    os.mkdir("public")
    copyDir("static", "public")

def copyDir(source, destination):
    log = logger()
    log.enable = True
    all_objects = os.listdir(source)
    for object in all_objects:
        log(f"Object: {object}")
        src_path = os.path.join(source, object)
        if os.path.isfile(src_path):
            log(f"Copy file: {object}")
            shutil.copy(src_path, destination)
            continue
        log(f"Copy dir: {object}")
        dest_path = os.path.join(destination, object)
        os.mkdir(dest_path)
        copyDir(src_path, dest_path)
    return 0

if __name__ == "__main__":
    main()