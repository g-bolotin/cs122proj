import arcade

class GalaxyYarn(arcade.Sprite):
    def __init__(self, center_x=0, center_y=0, direction=(0, 0), scale=1):
        super().__init__(center_x=center_x, center_y=center_y, scale=0.5)
        texture = arcade.load_texture("../assets/powerups/galaxy-ball-64.png")
        self.texture = texture
        self.center_x, self.center_y = center_x, center_y
        self.change_x = direction[0] * 15  # speed
        self.change_y = direction[1] * 15

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
