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
        self.scene = None

    def setup(self):
        arcade.set_background_color(arcade.color.BLUE_YONDER)

        # Initialize Scene
        self.scene = arcade.Scene()

        # Create the Sprite lists
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite("Player", self.player_sprite)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite,
            arcade.SpriteList()
        )

    def on_draw(self):
        arcade.start_render()

        # Draw our Scene
        self.scene.draw()

        sidebar_width = 110
        arcade.draw_lrtb_rectangle_filled(
            left=0,
            right=sidebar_width,
            bottom=0,
            top=constants.SCREEN_HEIGHT,
            color=arcade.color.BLACK
        )

        arcade.draw_text(
            "x" + str(constants.INITIAL_HEALTH),
            70,
            constants.SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            20 # font size
        )

    def on_update(self, delta_time):
        self.physics_engine.update()
        # self.player_list.update()
        self.player_sprite.update()
        self.player_sprite.update_animation()

    # WASD movement
    def on_key_press(self, key, modifiers):
        self.active_keys.add(key)
        self.update_movement()

    def on_key_release(self, key, modifiers):
        self.active_keys.discard(key)
        self.update_movement()

    def update_movement(self):
        x = 0
        y = 0
        if arcade.key.W in self.active_keys:
            y += 1
        if arcade.key.S in self.active_keys:
            y -= 1
        if arcade.key.A in self.active_keys:
            x -= 1
        if arcade.key.D in self.active_keys:
            x += 1

        # Normalize the vector if moving diagonally
        magnitude = (x ** 2 + y ** 2) ** 0.5
        if magnitude > 0:
            x = (x / magnitude) * MOVEMENT_SPEED
            y = (y / magnitude) * MOVEMENT_SPEED

        self.player_sprite.change_x = x
        self.player_sprite.change_y = y
