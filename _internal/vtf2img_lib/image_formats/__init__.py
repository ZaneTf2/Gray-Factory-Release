from typing import Type
import sys
import os

from .abgr8888  import ABGR8888
from .rgba8888 import RGBA8888
from .argb8888 import ARGB8888
from .bgr888 import BGR888
from .bgra8888 import BGRA8888
from .dxt1 import DXT1
from .dxt5 import DXT5
from .rgb888 import RGB888

from .abstract_format import AbstractFormat, registry

def resource_path(relative_path):
    try: base_path = sys._MEIPASS
    except Exception: base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def get_parser(image_format: int) -> Type[AbstractFormat]:
    for image_format_id, parser in registry.items():
        if image_format == image_format_id:
            return parser
        
__all__ = ["AbstractFormat", "get_parser"]
