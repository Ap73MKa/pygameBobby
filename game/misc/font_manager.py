from pygame import Surface, Color
from pygame.font import Font

from game.misc import PathManager

DEFAULT_FONT_PATH = PathManager.get("assets/graphics/hud/font.ttf")
DEFAULT_COLOR = (255, 255, 255)
DEFAULT_FONT_SIZE = 10


class FontManager:
    def __init__(self, font_path=DEFAULT_FONT_PATH, font_size=DEFAULT_FONT_SIZE):
        self.font = Font(font_path, font_size)

    def __render_text_shadow(
        self, surface: Surface, text: str, pos: tuple[int, int]
    ) -> None:
        text_shadow = self.font.render(text, False, (0, 0, 0))
        surface.blit(text_shadow, tuple(p + 1 for p in pos))

    def __render_text_surface(
        self,
        surface: Surface,
        text: str,
        pos: tuple[int, int],
        color: Color,
    ) -> None:
        text_surface = self.font.render(text, False, color)
        surface.blit(text_surface, pos)

    def get_text_center_x_pos(
        self, surface: Surface, text: str, y_position: int
    ) -> tuple[int, int]:
        text_width, _ = self.font.size(text)
        surface_width, _ = surface.get_size()
        x_position = (surface_width - text_width) // 2
        return x_position, y_position

    def render_text(
        self,
        surface: Surface,
        text: str,
        pos: tuple[int, int],
        color: Color = DEFAULT_COLOR,
        shadow: bool = True,
    ) -> None:
        if shadow:
            self.__render_text_shadow(surface, text, pos)
        self.__render_text_surface(surface, text, pos, color)
