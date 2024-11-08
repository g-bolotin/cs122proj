import arcade
from src import constants
from constants import RIGHT_FACING, LEFT_FACING, FRONT_FACING, BACK_FACING


class Player(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.textures = []
        self.center_x = constants.SCREEN_WIDTH / 2
        self.center_y = constants.SCREEN_HEIGHT / 2

        # Load player sprite textures
        # Left facing
        texture = arcade.load_texture("../assets/player/side-walk/cat-right-64-1.png", flipped_horizontally=True)
        self.textures.append(texture)

        # Right facing
        texture = arcade.load_texture("../assets/player/side-walk/cat-right-64-1.png")
        self.textures.append(texture)

        # Forward facing
        texture = arcade.load_texture("../assets/player/front-walk/cat-front-64-1.png")
        self.textures.append(texture)

        # By default, face forward.
        self.texture = texture

        # Backward facing
        texture = arcade.load_texture("../assets/player/back-walk/cat-back-64-1.png")
        self.textures.append(texture)

    def update(self):

        self.center_x += self.change_x
        self.center_y += self.change_y

        # Player facing direction based on movement
        if self.change_x < 0:                               # moving left on screen: face leftward
            self.texture = self.textures[LEFT_FACING]
        elif self.change_x > 0:                             # moving right on screen: face rightward
            self.texture = self.textures[RIGHT_FACING]
        elif self.change_y > 0:                             # moving up on screen: face backward
            self.texture = self.textures[BACK_FACING]
        elif self.change_y < 0:                             # moving down on screen: face forward
            self.texture = self.textures[FRONT_FACING]

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