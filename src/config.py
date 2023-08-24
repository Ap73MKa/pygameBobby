from dataclasses import dataclass


@dataclass
class Config:
    FPS: int = 60
    TITLE_SIZE: int = 16
    SCALE: int = 3
    WIDTH: int = TITLE_SIZE * 15
    HEIGHT: int = TITLE_SIZE * 12
    W_WIDTH: int = WIDTH * SCALE
    W_HEIGHT: int = HEIGHT * SCALE
    MAX_LEVEL: int = 7


configure = Config()
