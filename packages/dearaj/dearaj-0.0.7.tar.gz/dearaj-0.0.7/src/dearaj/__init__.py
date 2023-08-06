import sys
import pathlib

MODULE_PATH = pathlib.Path(__file__).parent.absolute()

sys.path.append(str(MODULE_PATH))

from local import *


__version__ = "0.0.7"

__all__ = [
    "core",
    "Conference",
    "Conferences",
    "MP",
    "MPList",
    "Speak",
    "Movie"
]
