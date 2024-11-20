import arcade
from src import constants
from player import Player
from constants import MOVEMENT_SPEED, TILE_SCALING, SIDEBAR_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT


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
        self.cat_head = None
        self.tile_map = None
        self.camera = None

    def setup(self):
        arcade.set_background_color(arcade.color.BLUE_YONDER)

        dock_tilemap = "../assets/environment/dock-stage.json"
        layer_options = {
            "Borders": {
                "use_spatial_hash": True,
            },
        }

        # Read in the tiled map
        self.tile_map = arcade.load_tilemap(dock_tilemap, TILE_SCALING, layer_options)

        # Initialize Scene with our TileMap, this will automatically add all layers
        # from the map as SpriteLists in the scene in the proper order.
        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # Create the Sprite lists
        self.scene.add_sprite_list("Player")
        self.scene.add_sprite("Player", self.player_sprite)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite,
            arcade.SpriteList()
        )

        self.cat_head = arcade.Sprite("../assets/player/cat-head.png")
        self.cat_head.center_x = 35
        self.cat_head.center_y = constants.SCREEN_HEIGHT - 30

        # Initialize camera
        self.camera = arcade.Camera(SCREEN_WIDTH + SIDEBAR_WIDTH, SCREEN_HEIGHT)

    def on_draw(self):
        arcade.start_render()

        # Use the camera to shift the game area
        self.camera.use()
        self.scene.draw()

        # Reset camera to default to draw the sidebar
        self.camera.use()
        arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

        # Draw sidebar
        arcade.draw_lrtb_rectangle_filled(
            left=0,
            right=SIDEBAR_WIDTH,
            bottom=0,
            top=constants.SCREEN_HEIGHT,
            color=arcade.color.BLACK
        )

        # Draw life counter icon
        self.cat_head.draw()

        # Draw life counter text
        arcade.draw_text(
            str(self.player_sprite.lives),
            80,
            constants.SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            35, # font size
            font_name=constants.FONT_NAME
        )

    def on_update(self, delta_time):
        self.physics_engine.update()
        # self.player_list.update()
        self.player_sprite.update()
        self.player_sprite.update_animation()

        # Keep the camera focused on the game area
        self.camera.move_to((-SIDEBAR_WIDTH, 0))

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
