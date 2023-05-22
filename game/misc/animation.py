from . import SpriteSheet


class Animation:
    def __init__(self, sprite_sheet: SpriteSheet, frame_speed: int):
        self.frame = 0
        self.frame_speed = frame_speed
        self.sprites = sprite_sheet
        self.frame_count = len(self.sprites[self.frame]) - 1

    def reset_frame(self):
        self.frame = 0

    def get_current_image(self, row: int = 0):
        return self.sprites[row][int(self.frame)]

    def animate(self, delta):
        self.frame += self.frame_speed * delta
        self.frame %= self.frame_count
