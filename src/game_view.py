import arcade
from src import constants
from player import Player
from constants import MOVEMENT_SPEED
class GameView(arcade.View):
    def __init__(self):
        super().__init__()

        self.player_sprite = None
        self.physics_engine = None
        self.player_list = None

    def setup(self):
        arcade.set_background_color(arcade.color.BLUE_YONDER)

        self.player_list = arcade.SpriteList()

        # Create player sprite at screen center
        self.player_sprite = Player(
            # MOVED TO PLAYER CLASS
            # filename="../assets/player/cat-front-64-1.png",  # Temporary sprite
            # image_width=32, potential sprite width
            # image_height=32, potential sprite height
            # center_x=constants.SCREEN_WIDTH / 2,
            # center_y=constants.SCREEN_HEIGHT / 2,
        )
        self.player_list.append(self.player_sprite)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite,
            arcade.SpriteList()
        )

    def on_draw(self):
        arcade.start_render()
        # Activate the camera
        self.player_list.draw()

        arcade.draw_text(
            "Lives: 5",
            10,
            constants.SCREEN_HEIGHT - 20,
            arcade.color.WHITE,
            14 # font size
        )

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.player_list.update()

    # WASD movement
    def on_key_press(self, key, modifiers):
        if key == arcade.key.W:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.S:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.A:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.D:
            self.player_sprite.change_x = MOVEMENT_SPEED

    # Stop movement
    def on_key_release(self, key, modifiers):
        if key in (arcade.key.W, arcade.key.S):
            self.player_sprite.change_y = 0
        elif key in (arcade.key.A, arcade.key.D):
            self.player_sprite.change_x = 0