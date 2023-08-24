from collections.abc import Sequence

from pygame.math import Vector2
from pygame.sprite import Group, Sprite
from pygame.surface import Surface

from src.config import Config
from src.objects import Player


class CameraGroup(Group):
    def __init__(self):
        super().__init__()
        self.size = Vector2((Config.WIDTH, Config.HEIGHT))
        self.camera = self.size / 2
        self.camera_speed = 3 * 100
        self.offset = Vector2()
        self.render_texture = Surface(self.size)

    def _is_visible(self, sprite) -> bool:
        return (
            self.size.y + self.offset.y
            > sprite.rect.y
            > -Config.TITLE_SIZE - self.offset.y
            and self.size.x + self.offset.x
            > sprite.rect.x
            > -Config.TITLE_SIZE - self.offset.x
        )

    def _get_offset_sprites(self) -> Sequence[tuple[Sprite, Vector2]]:
        return [
            (sprite, sprite.rect.topleft - self.offset)
            for sprite in self.sprites()
            if self._is_visible(sprite)
        ]

    def _update_camera_pos(self, player: Player, delta: float) -> None:
        heading = player.rect.center - self.camera
        distance = heading.length()
        if distance > 0:
            speed = min(self.camera_speed * delta, distance)
            heading.scale_to_length(speed)
            self.camera += heading

    def _clamp_offset(self, corner: Vector2) -> None:
        self.offset = self.camera - (self.size / 2)
        self.offset.x = max(0, min(int(self.offset.x), corner.x - self.size.x))
        self.offset.y = max(0, min(int(self.offset.y), corner.y - self.size.y))
        self.offset = Vector2(round(self.offset.x), round(self.offset.y))

    def custom_update(self, player: Player, corner: Vector2, delta: float) -> None:
        self._update_camera_pos(player, delta)
        self._clamp_offset(corner)

    def custom_render(self, surface: Surface) -> None:
        self.render_texture.fill((0, 0, 0))
        for sprite, offset_pos in self._get_offset_sprites():
            self.render_texture.blit(sprite.image, offset_pos)
        surface.blit(self.render_texture, (0, 0))
