import arcade
from arcade import SpriteList

from src import constants
from player import Player
from constants import MOVEMENT_SPEED, TILE_SCALING, SIDEBAR_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT
import random

from src.enemies.enemy import ENEMY_SPEED_IN_PIXELS
from src.enemies.fishhead import Fishhead


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
        self.astar_barrier_list = None
        self.enemy_path_list = []
        self.yarn_ball_list = self.player_sprite.yarn_balls

    def setup(self):
        arcade.set_background_color(arcade.color.BLUE_YONDER)

        dock_tilemap = "../assets/environment/tiled_tilemaps/dock-stage.json"
        layer_options = {
            "Borders": {
                "use_spatial_hash": True
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
        self.scene.add_sprite_list("Enemies")

        # Add borders and walls from tilemap (to add more walls or edit borders, open the tilesheet in Tiled)
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite,
            walls=self.scene["Borders"]
        )

        # Pathfinding Wall List
        self.astar_barrier_list = arcade.AStarBarrierList(
            blocking_sprites=self.scene["Borders"],
            grid_size=48,
            moving_sprite=self.player_sprite,
            left=-48,
            right=SCREEN_WIDTH + 48,
            top=SCREEN_HEIGHT + 48,
            bottom=-48

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

        # Draw borders for debugging
        # for barrier in self.astar_barrier_list.blocking_sprites:
        #     arcade.draw_rectangle_outline(
        #         barrier.center_x, barrier.center_y,
        #         48, 48, arcade.color.RED
        #     )

        self.player_sprite.yarn_balls.draw()

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
        self.player_sprite.update()
        self.player_sprite.update_animation()
        self.player_sprite.yarn_balls.update()

        # Each tile is 48x48 (originally 64x64 but scaled by 0.75)
        top_coords = {'x': 268, 'y': 0}
        bottom_coords = {'x': 268, 'y': SCREEN_HEIGHT-1}
        left_coords = {'x': 0, 'y': 268}  # no idea why this one doesn't require offset by sidebar
        right_coords = {'x': SCREEN_WIDTH-SIDEBAR_WIDTH, 'y': 268}
        coords = [top_coords, bottom_coords, left_coords, right_coords]

        # Randomly select enemy spawning time and position
        if random.random() < 0.01:              # Time
            spawn_pos = random.randint(0, 3)    # Spawn position: top, bottom, left, right
            tile_num = random.randint(1, 4)     # Tile: one of 4 tiles
            position = coords[spawn_pos]        # Appropriate coordinates for the selected spawn position

            # Tile multiplier - get next 3 tiles beyond the topmost or leftmost one
            x_mult = 0
            y_mult = 0
            if spawn_pos < 2:
                x_mult = tile_num
            else:
                y_mult = tile_num

            enemy = Fishhead(
                center_x=position.get('x') + (48 * x_mult),
                center_y=position.get('y') + (48 * y_mult),
                scale=0.75
            )
            self.scene["Enemies"].append(enemy)

        # Keep the camera focused on the game area
        self.camera.move_to((-SIDEBAR_WIDTH, 0))

        for e in self.scene["Enemies"]:
            e.update_path(self.player_sprite, self.astar_barrier_list, delta_time)
            e.follow_path(ENEMY_SPEED_IN_PIXELS, delta_time)
            e.update_animation()

        for yarn_ball in self.yarn_ball_list:
            # Check collision
            enemies_hit = arcade.check_for_collision_with_list(yarn_ball, self.scene["Enemies"])
            for enemy in enemies_hit:
                enemy.take_damage()
                yarn_ball.kill()

    # WASD movement
    def on_key_press(self, key, modifiers):
        self.active_keys.add(key)
        self.update_movement()

        # shoot yarn ball
        if key == arcade.key.SPACE:
            self.player_sprite.shoot()

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
