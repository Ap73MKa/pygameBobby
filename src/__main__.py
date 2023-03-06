from pygame import quit as game_quit, Surface, SurfaceType
from pygame import init, DOUBLEBUF, QUIT, display
from pygame.display import set_caption, set_mode
from pygame.event import get as get_event
from pygame.time import Clock

from src.misc.config import Config
from src.scene.stages.menu import Menu
from src.scene.stages.gameplay import Gameplay
from src.scene.stages.pause import Pause
from src.scene.stages.stage_utils import GameStage


class Game:
    def __init__(self) -> None:
        self._running = True
        self.size = self.width, self.height = Config.WIDTH, Config.HEIGHT
        self.screen = self.on_init()
        self.clock = Clock()
        self.stages = {
            GameStage.MENU: Menu(),
            GameStage.GAMEPLAY: Gameplay(),
            GameStage.PAUSE: Pause(),
        }
        self.stage = self.stages[GameStage.MENU]

    def flip_state(self) -> None:
        self.stage.done = False
        self.stage = self.stages[self.stage.next_state]
        self.stage.startup(self.stage.persist)

    def on_init(self) -> Surface | SurfaceType:
        init()
        set_caption("Bobby Carrot")
        return set_mode(self.size, DOUBLEBUF)

    def on_event(self) -> None:
        for event in get_event():
            self._running = not event.type == QUIT
            self.stage.get_event(event)

    def on_update(self, delta) -> None:
        if self.stage.quit:
            self._running = False
        elif self.stage.done:
            self.flip_state()
        self.stage.update(delta)

    def on_render(self) -> None:
        self.stage.render()
        display.update()

    def on_execute(self) -> None:
        delta = 0
        while self._running:
            self.on_event()
            self.on_update(delta)
            self.on_render()
            delta = self.clock.tick(Config.FPS) / 1000
        game_quit()


if __name__ == "__main__":
    game = Game()
    game.on_execute()
