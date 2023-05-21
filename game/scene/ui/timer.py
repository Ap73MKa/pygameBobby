from pygame import time, Surface

from game.misc import FontManager


class Timer:
    def __init__(self):
        self.start_time = time.get_ticks()
        self.elapsed_time = 0
        self.text = "00:00"
        self.font_manager = FontManager()

    def __update_timer_text(self) -> None:
        minutes = self.elapsed_time // 60000
        seconds = (self.elapsed_time % 60000) // 1000
        self.text = f"{minutes:02d}:{seconds:02d}"

    def reset_time(self) -> None:
        self.elapsed_time = 0
        self.start_time = time.get_ticks()

    def update(self) -> None:
        self.elapsed_time = time.get_ticks() - self.start_time
        self.__update_timer_text()

    def render(self, surface: Surface) -> None:
        self.font_manager.render_text(surface, self.text, (2, 2))
