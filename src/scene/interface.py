from pygame import Surface

from src.scene.ui import CarrotCounter, Timer


class Interface:
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
