import cProfile
from sys import exit
from pygame import Surface, display, init, QUIT
from pygame.display import set_caption, set_mode, set_icon
from pygame.event import get as events
from pygame.image import load
from pygame.time import Clock
from pygame.transform import scale

from game.misc import Config, PathManager
from game.scene import StateManager
from game.scene.sound_manager import SoundManager


class Game:
    def __init__(self):
        self._running = True
        self.size = Config.W_WIDTH, Config.W_HEIGHT
        self.game_canvas = Surface((Config.WIDTH, Config.HEIGHT))
        self.screen = None
        self.clock = Clock()
        self.initialize()
        self.manager = StateManager()

    def initialize(self) -> None:
        init()
        set_caption("Bobby Carrot")
        set_icon(load(PathManager.get("assets/graphics/icon.png")))
        self.screen = set_mode(self.size)
        SoundManager().play_sound("background_music", -1)

    def handle_event(self) -> None:
        for event in events():
            self._running = event.type == QUIT
            self.manager.get_event(event)

    def update(self, delta: float) -> None:
        self._running = self.manager.is_running()
        self.manager.update(delta)

    def render(self) -> None:
        self.manager.render(self.game_canvas)
        self.screen.blit(scale(self.game_canvas, self.size), (0, 0))
        display.update()

    def run(self) -> None:
        while self._running:
            delta = self.clock.tick_busy_loop(Config.FPS) / 1000.0
            self.handle_event()
            self.update(delta)
            self.render()
        exit()


if __name__ == "__main__":
    game = Game()
    game.run()
