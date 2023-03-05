from abc import ABC
from typing import Final


class Config(ABC):
    FPS: Final = 60
    TITLE_SIZE: Final = 32
    WIDTH: Final = TITLE_SIZE * 17
    HEIGHT: Final = TITLE_SIZE * 12
