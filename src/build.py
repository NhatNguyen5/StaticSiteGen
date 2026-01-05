import os
import shutil
from logging_module.my_logging import logger

def copyDir(source, destination):
    log = logger()
    log.enable = True
    all_objects = os.listdir(source)
    for object in all_objects:
        src_path = os.path.join(source, object)
        if os.path.isfile(src_path):
            log(f"Copy file: {src_path} to {destination}")
            shutil.copy(src_path, destination)
            continue
        dest_path = os.path.join(destination, object)
        os.mkdir(dest_path)
        log(f"Copy dir: from {src_path} to {dest_path}")
        copyDir(src_path, dest_path)
    return 0