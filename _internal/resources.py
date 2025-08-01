import sys
import os
import re
from pathlib import Path

Debug = False

def resource_path():
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    path = os.path.abspath(f"{base_path}")
    return re.sub(r"[\\]", "/", path)

if(Debug):
    print(f"[DEBUG : Resources] resources path : {resource_path()}")

def resources():
    return Path(resource_path())