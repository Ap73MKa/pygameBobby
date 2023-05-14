import pygame as pg
from pygame import Surface
from pygame.display import set_caption, set_mode, set_icon
from pygame.event import get as events
from pygame.image import load
from pygame.time import Clock
from pygame.transform import scale

from game.misc import Config, PathManager
from game.scene import StateManager
from game.scene.sound_manager import SoundManager


class Game:
    def __init__(self) -> None:
        self._running = True
        self.size = self.width, self.height = Config.W_WIDTH, Config.W_HEIGHT
        self.game_canvas = Surface((Config.WIDTH, Config.HEIGHT))
        self.screen = None
        self.clock = Clock()
        self.load_background_music()
        self.initialize()
        self.manager = StateManager()

    def initialize(self) -> None:
        pg.init()
        set_caption("Bobby Carrot")
        set_icon(load(PathManager.get("assets/graphics/icon.png")))
        self.screen = set_mode(self.size, pg.DOUBLEBUF)

    def load_background_music(self):
        SoundManager().play_sound('background_music', -1)

    def handle_event(self) -> None:
        for event in events():
            self._running = event.type == pg.QUIT
            self.manager.get_event(event)

    def update(self, delta) -> None:
        self._running = self.manager.is_running()
        self.manager.update(delta)

    def render(self) -> None:
        self.manager.render(self.game_canvas)
        self.screen.blit(scale(self.game_canvas, self.size), (0, 0))
        pg.display.update()

    def run(self) -> None:
        delta = 0.0
        while self._running:
            self.handle_event()
            self.update(delta)
            self.render()
            delta = self.clock.tick(Config.FPS) / 1000
        pg.quit()


if __name__ == "__main__":
    game = Game()
    game.run()
