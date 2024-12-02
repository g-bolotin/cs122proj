import arcade
from src.utils import get_resource_path

class YarnBall(arcade.Sprite):
    def __init__(self, direction, player_position):
        super().__init__(get_resource_path("assets/player/yarn-ball.png"), scale=0.5)
        self.center_x, self.center_y = player_position
        self.change_x = direction[0] * 10 # speed
        self.change_y = direction[1] * 10

    def update(self):
        self.center_x += self.change_x
        self.center_y += self.change_y
