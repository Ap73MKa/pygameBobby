import pygame as pg

from misc.config import Config
from src.scenes.stages.menu import Menu
from src.scenes.stages.gameplay import Gameplay
from src.scenes.stages.pause import Pause
from src.scenes.stages.stage_utils import GameStage


class Game:
    def __init__(self):
        self._running = True
        self.size = self.width, self.height = Config.WIDTH, Config.HEIGHT
        self.screen = self.on_init()
        self.clock = pg.time.Clock()
        self.stages = {
            GameStage.MENU: Menu(),
            GameStage.GAMEPLAY: Gameplay(),
            GameStage.PAUSE: Pause()}
        self.stage = self.stages[GameStage.MENU]

    def flip_state(self):
        self.stage.done = False
        self.stage = self.stages[self.stage.next_state]
        self.stage.startup(self.stage.persist)

    def on_init(self):
        pg.init()
        pg.display.set_caption('Bobby Carrot')
        return pg.display.set_mode(self.size, pg.DOUBLEBUF)

    def on_event(self):
        for event in pg.event.get():
            self._running = not event.type == pg.QUIT
            self.stage.get_event(event)

    def on_update(self, delta):
        if self.stage.quit:
            self._running = False
        elif self.stage.done:
            self.flip_state()
        self.stage.update(delta)

    def on_render(self):
        self.stage.render()
        pg.display.update()

    def on_execute(self) -> None:
        delta = 0
        while self._running:
            self.on_event()
            self.on_update(delta)
            self.on_render()
            delta = self.clock.tick(Config.FPS) / 1000
        pg.quit()


if __name__ == '__main__':
    game = Game()
    game.on_execute()
