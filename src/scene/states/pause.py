from pygame import K_DOWN, K_RETURN, K_UP, KEYUP, QUIT, Color, Rect, Surface
from pygame.event import Event
from pygame.image import load

from src.config import configure
from src.misc import PathManager
from src.scene.states.stage_utils import GameState
from src.scene.states.state import State


class Pause(State):
    def __init__(self) -> None:
        super().__init__()
        self.bg_tile = load(PathManager.get("assets/graphics/hud/grass.png")).convert()
        self.center = (configure.WIDTH // 2, configure.HEIGHT // 2)
        self.active_index = 0
        self.options = ["Continue", "Reload level", "Back to menu", "Exit"]
        self.is_drawn_once = False
        self.persist = {}
        self.actions = {
            0: (GameState.GAMEPLAY, {"reload": False}),
            1: (GameState.GAMEPLAY, {"reload": True}),
            2: (GameState.MENU, {}),
            3: (None, None),
        }
        self.key_actions = {
            K_UP: lambda: self.handle_option_index(-1),
            K_DOWN: lambda: self.handle_option_index(1),
            K_RETURN: lambda: self.handle_action(),
        }

    def startup(self, persistent: dict) -> None:
        self.active_index = 0
        self.is_drawn_once = False

    def handle_action(self) -> None:
        self.sound_manager.play_sound("menu_sound")
        next_state, persist = self.actions[self.active_index]
        if next_state is None:
            self.quit = True
            return
        self.next_state = next_state
        self.persist = persist
        self.done = True

    def handle_option_index(self, move: int = 0) -> None:
        self.active_index = (self.active_index + move) % len(self.options)

    def render_menu_text(
        self, surface: Surface, index, y_pos: int, color: Color = (255, 255, 255)
    ):
        color = (100, 100, 100) if index != self.active_index else color
        pos = self.get_menu_text_position(surface, y_pos, self.options[index], index)
        self.font_manager.render_text(surface, self.options[index], pos, color)

    def get_menu_text_position(
        self, surface: Surface, y_pos: int, text: str, index: int
    ) -> tuple[int, int]:
        pos = self.font_manager.get_text_center_x_pos(surface, text, y_pos)
        return pos[0], pos[1] + (index * 20)

    def get_text_position(self, text, index) -> Rect:
        center = (self.center[0], self.center[1] - 30 + (index * 20))
        return text.get_rect(center=center)

    def handle_event(self, event: Event) -> None:
        if event.type == QUIT:
            self.quit = True
        elif event.type == KEYUP:
            if action := self.key_actions.get(event.key):
                action()

    @staticmethod
    def draw_black_surface(game_surface: Surface) -> None:
        dark = Surface((configure.WIDTH, configure.HEIGHT))
        dark.fill((0, 0, 0))
        dark.set_alpha(100)
        game_surface.blit(dark, (0, 0))

    def render(self, game_surface: Surface) -> None:
        if not self.is_drawn_once:
            self.is_drawn_once = True
            self.draw_black_surface(game_surface)

        for index in range(len(self.options)):
            self.render_menu_text(
                game_surface, index, game_surface.get_rect().centery - 30
            )
