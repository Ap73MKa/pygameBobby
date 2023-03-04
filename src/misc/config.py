from abc import ABC
from typing import Final


class Config(ABC):
    WIDTH: Final = 800
    HEIGHT: Final = 600
    FPS: Final = 32
    TITLE_SIZE: Final = 32
