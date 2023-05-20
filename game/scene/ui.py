from pygame import Surface, time, image

from game.misc import Config, PathManager, FontManager


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


class CarrotCounter:
    def __init__(self):
        self.carrot_img = image.load(PathManager.get("assets/graphics/hud/carrot.png"))
        self.font_manager = FontManager()
        self.count = 0

    def update(self, count: int) -> None:
        self.count = count

    def render(self, surface: Surface) -> None:
        if self.count > 0:
            self.font_manager.render_text(
                surface,
                str(self.count),
                (Config.WIDTH - Config.TITLE_SIZE * 2, 2),
            )
            surface.blit(self.carrot_img, (Config.WIDTH - Config.TITLE_SIZE, 2))


class UI:
    def __init__(self):
        self.timer = Timer()
        self.carrot_counter = CarrotCounter()

    def get_time(self) -> str:
        return self.timer.text

    def reset(self) -> None:
        self.carrot_counter.count = 0
        self.timer.reset_time()

    def update(self, carrot_count: int) -> None:
        self.timer.update()
        self.carrot_counter.update(carrot_count)

    def render(self, surface: Surface) -> None:
        self.timer.render(surface)
        self.carrot_counter.render(surface)
