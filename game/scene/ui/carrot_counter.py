from pygame import image, Surface

from game.misc import PathManager, FontManager, Config


class CarrotCounter:
    def __init__(self):
        image_path = "assets/graphics/hud/carrot.png"
        self.carrot_img = image.load(PathManager.get(image_path))
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
