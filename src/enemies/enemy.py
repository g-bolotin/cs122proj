import arcade
from src import constants
from arcade import FACE_RIGHT, FACE_LEFT, FACE_UP, FACE_DOWN

from src.constants import LEVEL_BORDER_SIZE, SIDEBAR_WIDTH


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

        # Pathfinding
        self.path = None

    def update(self):

        # Edge of screen collision Logic
        super().update()
        if self.left < LEVEL_BORDER_SIZE:
            self.left = LEVEL_BORDER_SIZE
        # Adjust collision to take sidebar offset into account
        elif self.right > constants.SCREEN_WIDTH - 1 - SIDEBAR_WIDTH - LEVEL_BORDER_SIZE:
            self.right = constants.SCREEN_WIDTH - 1 - SIDEBAR_WIDTH - LEVEL_BORDER_SIZE

        if self.bottom < LEVEL_BORDER_SIZE:
            self.bottom = LEVEL_BORDER_SIZE
        elif self.top > constants.SCREEN_HEIGHT - 1 - LEVEL_BORDER_SIZE:
            self.top = constants.SCREEN_HEIGHT - 1 - LEVEL_BORDER_SIZE

    # def update_path(self, player_sprite, delta_time):
    #     self.path