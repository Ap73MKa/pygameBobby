from abc import ABC
from typing import Final


class Config(ABC):
    FPS: Final = 30
    TITLE_SIZE: Final = 16
    SCALE: Final = 3
    WIDTH: Final = TITLE_SIZE * 15
    HEIGHT: Final = TITLE_SIZE * 12
    W_WIDTH: Final = WIDTH * SCALE
    W_HEIGHT: Final = HEIGHT * SCALE
    MAX_LEVEL: Final = 7
