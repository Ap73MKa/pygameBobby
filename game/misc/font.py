from pygame import Surface
from pygame.font import Font


def get_text_center_x_pos(surface: Surface, font: Font, text: str, y_position: int) -> tuple[int, int]:
    text_width, _ = font.size(text)
    surface_width, _ = surface.get_size()
    x_position = (surface_width - text_width) // 2
    return x_position, y_position
