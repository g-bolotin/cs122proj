import arcade
from src import constants
from arcade import FACE_RIGHT, FACE_LEFT, FACE_UP, FACE_DOWN

class Enemy(arcade.Sprite):
    def __init__(self, center_x=0, center_y=0, scale=1):
        super().__init__(scale=scale, center_x=center_x, center_y=center_y)

        self.state = FACE_DOWN   # player directionality
        self.time_counter = 0.0  # for controlling animation frame rate

        # Sprite size
        self.width = 64
        self.height = 64

        # Walking textures
        self.walk_left_textures = []
        self.walk_right_textures = []
        self.walk_up_textures = []
        self.walk_down_textures = []

        # List of all walk texture categories -- allows access to correct walking direction by direction state
        self.walk_textures = [
            self.walk_right_textures,
            self.walk_left_textures,
            self.walk_up_textures,
            self.walk_down_textures
        ]

    def update(self):

        # Edge of screen collision Logic
        super().update()
        if self.left < 0:
            self.left = 0
        elif self.right > constants.SCREEN_WIDTH - 1:
            self.right = constants.SCREEN_WIDTH - 1

        if self.bottom < 0:
            self.bottom = 0
        elif self.top > constants.SCREEN_HEIGHT - 1:
            self.top = constants.SCREEN_HEIGHT - 1
