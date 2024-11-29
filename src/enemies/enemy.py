import arcade
from src import constants
from arcade import FACE_RIGHT, FACE_LEFT, FACE_UP, FACE_DOWN

from src.constants import LEVEL_BORDER_SIZE, SIDEBAR_WIDTH, MOVEMENT_SPEED

ENEMY_SPEED_IN_PIXELS = 48
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

        self.health = 3

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

    # Rudimentary pathfinding, override to implement movement
    def update_path(self, player_sprite, wall_list, delta_time):

        self.path = arcade.astar_calculate_path(
            start_point=self.position,
            end_point=player_sprite.position,
            astar_barrier_list=wall_list,
            diagonal_movement=False
        )
        if self.path:
            print(self.path)

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()