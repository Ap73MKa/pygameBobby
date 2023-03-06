from abc import ABC
from typing import Final


class Config(ABC):
    FPS: Final = 60
    TITLE_SIZE: Final = 48
    WIDTH: Final = TITLE_SIZE * 15
    HEIGHT: Final = TITLE_SIZE * 12
    MAX_LEVEL: Final = 4
