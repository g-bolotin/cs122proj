import arcade
from src import constants
from player import Player
from constants import MOVEMENT_SPEED


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.active_keys = set()

        # Create player sprite at screen center
        self.player_sprite = Player(
            center_x=constants.SCREEN_WIDTH / 2,
            center_y=constants.SCREEN_HEIGHT / 2,
            scale=1
        )
        self.physics_engine = None
        self.player_list = None

    def setup(self):
        arcade.set_background_color(arcade.color.BLUE_YONDER)

        self.player_list = arcade.SpriteList()
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
            "Lives: " + str(constants.INITIAL_HEALTH),
            10,
            constants.SCREEN_HEIGHT - 20,
            arcade.color.BLACK,
            18 # font size
        )

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.player_list.update()
        self.player_sprite.update()
        self.player_sprite.update_animation()

    # WASD movement
    def on_key_press(self, key, modifiers):
        self.active_keys.add(key)
        if key == arcade.key.W or arcade.key.S in self.active_keys:
            self.player_sprite.change_y = MOVEMENT_SPEED if arcade.key.W in self.active_keys else -MOVEMENT_SPEED
        if key == arcade.key.A or arcade.key.D in self.active_keys:
            self.player_sprite.change_x = MOVEMENT_SPEED if arcade.key.D in self.active_keys else -MOVEMENT_SPEED

    # Stop movement
    def on_key_release(self, key, modifiers):
        self.active_keys.discard(key)
        if key in (arcade.key.W, arcade.key.S):
            if arcade.key.W in self.active_keys:
                self.player_sprite.change_y = MOVEMENT_SPEED
            elif arcade.key.S in self.active_keys:
                self.player_sprite.change_y = -MOVEMENT_SPEED
            else:
                self.player_sprite.change_y = 0
        if key in (arcade.key.A, arcade.key.D):
            if arcade.key.A in self.active_keys:
                self.player_sprite.change_x = -MOVEMENT_SPEED
            elif arcade.key.D in self.active_keys:
                self.player_sprite.change_x = MOVEMENT_SPEED
            else:
                self.player_sprite.change_x = 0