import arcade

from src import constants, music_player
from src.music_player import MusicManager
from src.powerups.galaxy_yarn import GalaxyYarn
from src.views.game_over_view import GameOverView

from src.player import Player
from src.constants import MOVEMENT_SPEED, TILE_SCALING, SIDEBAR_WIDTH, SCREEN_WIDTH, SCREEN_HEIGHT, FONT_NAME
import random

from src.enemies.enemy import ENEMY_SPEED_IN_PIXELS
from src.enemies.fishhead import Fishhead
from src.enemies.boss_fish import BossFish
from src.views.win_view import WinView
from src.utils import get_resource_path
from arcade import Sound


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.sfx_player = None
        self.active_keys = set()

        # Create player sprite at screen center
        self.player_sprite = Player(
            center_x=SCREEN_WIDTH / 2,
            center_y=SCREEN_HEIGHT / 2,
            scale=1
        )

        self.physics_engine = None
        self.scene = None
        self.cat_head = None
        self.tile_map = None
        self.camera = None
        self.music = None

        # Enemies
        self.astar_barrier_list = None
        self.enemy_path_list = []
        self.yarn_ball_list = self.player_sprite.yarn_balls
        self.enemy_spawn_rate = 0.01

        # Powerup tracking
        self.powerup_count = None
        self.powerup_icon = None
        self.powerup_timer = 0.0
        self.powerup_active = False

        # Level Timer
        self.remaining_time = 10.0
        self.timer_text = None

        # Boss
        self.boss_spawned = False
        self.boss_defeated = False
        self.boss_health = None

    def setup(self):
        MusicManager.stop_music() # note: cannot stop music from previous view, will stop all music
        self.music = get_resource_path("assets/sfx/in-game.wav")
        MusicManager.play_music(self.music, loop=True)

        arcade.set_background_color(arcade.color.BLUE_YONDER)

        dock_tilemap = get_resource_path("assets/environment/tiled_tilemaps/dock-stage.json")
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
        self.scene.add_sprite_list("Powerups", use_spatial_hash=True)
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

        self.cat_head = arcade.Sprite(get_resource_path("assets/player/cat-head.png"))
        self.cat_head.center_x = 35
        self.cat_head.center_y = SCREEN_HEIGHT - 30

        self.powerup_icon = arcade.Sprite("../assets/powerups/galaxy-ball-64.png")
        self.powerup_icon.scale = 0.55
        self.powerup_icon.center_x = 35
        self.powerup_icon.center_y = constants.SCREEN_HEIGHT - 170

        # Level timer text
        self.timer_text = arcade.Text(
            text="1:00",
            start_x=55,
            start_y=SCREEN_HEIGHT - 90,
            color=arcade.color.WHITE,
            font_size=35,
            anchor_x="center",
            font_name=FONT_NAME
        )

        # Boss Health Text
        self.boss_health = arcade.Text(
            text="30/30",
            start_x=55,
            start_y=SCREEN_HEIGHT - 130,
            color=arcade.color.RED,
            font_size=35,
            anchor_x="center",
            font_name=constants.FONT_NAME
        )

        # Powerup Counter
        self.powerup_count = arcade.Text(
            text="0",
            start_x=90,
            start_y=SCREEN_HEIGHT - 180,
            color=arcade.color.CYAN,
            font_size=35,
            anchor_x="center",
            font_name=constants.FONT_NAME,
        )

        # Initialize camera
        self.camera = arcade.Camera(SCREEN_WIDTH + SIDEBAR_WIDTH, SCREEN_HEIGHT)

        self.scene.add_sprite_list("Boss")

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

        # Draw yarn balls before camera reset
        self.player_sprite.yarn_balls.draw()

        # Reset camera to default to draw the sidebar
        self.camera.use()
        arcade.set_viewport(0, SCREEN_WIDTH, 0, SCREEN_HEIGHT)

        # Draw sidebar
        arcade.draw_lrtb_rectangle_filled(
            left=0,
            right=SIDEBAR_WIDTH,
            bottom=0,
            top=SCREEN_HEIGHT,
            color=arcade.color.BLACK
        )

        # Draw life counter icon
        self.cat_head.draw()

        # Draw life counter text
        arcade.draw_text(
            str(self.player_sprite.lives),
            80,
            SCREEN_HEIGHT - 40,
            arcade.color.WHITE,
            35, # font size
            font_name=FONT_NAME
        )

        # Draw timer text
        self.timer_text.draw()

        if self.boss_spawned:
            self.boss_health.draw()

        self.powerup_icon.draw()
        self.powerup_count.draw()

    def on_update(self, delta_time):
        self.physics_engine.update()
        self.player_sprite.update()
        self.player_sprite.update_animation()
        self.player_sprite.yarn_balls.update()

        # Powerup timer, disable powerup after 5 seconds
        if self.powerup_active:
            self.powerup_timer += delta_time
            if self.powerup_timer >= 5:
                self.powerup_active = False
                self.powerup_timer = 0.0

        # Ensure the timer doesn't go into negatives
        # Check time to spawn boss
        if not self.boss_spawned:
            # Subtract delta_time from remaining_time
            self.remaining_time -= delta_time

            # Once timer runs out, spawn boss
            if self.remaining_time <= 0:
                self.remaining_time = 0

                boss_spawn_position = self.get_enemy_spawn_position()
                boss = BossFish(
                    center_x=boss_spawn_position[0],
                    center_y=boss_spawn_position[1],
                    scale=2
                )
                self.scene["Boss"].append(boss)
                self.boss_spawned = True
                self.enemy_spawn_rate = 0.01

                # Change time to indicate Boss level
                self.timer_text.text = "BOSS"
                self.timer_text.color = arcade.color.WHITE

            else:
                # Calculate minutes and seconds
                minutes = int(self.remaining_time) // 60
                seconds = int(self.remaining_time) % 60

                # Update the timer text
                self.timer_text.text = f"{minutes:01d}:{seconds:02d}"

                # Increase enemy spawn rate halfway through level
                if self.remaining_time <= 30:
                    self.timer_text.color = arcade.color.GOLD
                    self.enemy_spawn_rate = 0.02

                # Change text color to indicate last 10s before level complete
                if self.remaining_time <= 10:
                    self.timer_text.color = arcade.color.RED
                    self.enemy_spawn_rate = 0.03
        else:
            # boss has spawned
            pass

        # Spawn enemies continuously until boss spawns
        if not self.boss_spawned:
            self.spawn_regular_enemies()

        # Spawn powerups occasionally if there isn't one on screen already
        if len(self.scene["Powerups"]) < 1:
            self.spawn_powerup()

        # Player picks up powerup
        powerup_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.scene["Powerups"]
        )

        for powerup in powerup_hit_list:
            powerup.remove_from_sprite_lists()
            pickup_sfx = Sound(get_resource_path("assets/sfx/pickup.wav"))
            self.sfx_player = arcade.play_sound(pickup_sfx)
            self.player_sprite.inventory.append(powerup)
            num_powerups = len(self.player_sprite.inventory)
            self.powerup_count.text = f"{num_powerups:01d}"

        # Keep the camera focused on the game area
        self.camera.move_to((-SIDEBAR_WIDTH, 0))

        # only check for collisions if player is not blinking (invincibility frames)
        if not self.player_sprite.is_blinking:
            # Check collision of player and enemy
            enemies_attack = arcade.check_for_collision_with_list(self.player_sprite, self.scene["Enemies"])
            if enemies_attack:
                self.player_sprite.lives -= 1
                if self.player_sprite.lives <= 0:
                    # When player dies
                    game_over_view = GameOverView()
                    self.window.show_view(game_over_view)
                    return
                else:
                    # Respawn at center
                    self.player_sprite.center_x = SCREEN_WIDTH / 2
                    self.player_sprite.center_y = SCREEN_HEIGHT / 2

                    # Blink player to indicate lost life
                    self.player_sprite.is_blinking = True
                    self.player_sprite.blink_timer = 2
                    return

            # Check boss collision
            if self.boss_spawned:
                for boss in self.scene["Boss"]:
                    if arcade.check_for_collision(self.player_sprite, boss):
                        self.player_sprite.lives -= 1
                        if self.player_sprite.lives <= 0:
                            game_over_view = GameOverView()
                            self.window.show_view(game_over_view)
                            return
                        else:
                            # When player loses a life
                            self.player_sprite.center_x = SCREEN_WIDTH / 2
                            self.player_sprite.center_y = SCREEN_HEIGHT / 2
                            self.player_sprite.is_blinking = True
                            self.player_sprite.blink_timer = 2
                            return

        # Player blinking
        if self.player_sprite.is_blinking:
            self.player_sprite.blink_timer -= delta_time
            if self.player_sprite.blink_timer <= 0:
                self.player_sprite.is_blinking = False
                self.player_sprite.alpha = 255  # Ensure visibility after blinking ends
            else:
                # Toggle visibility over a time interval
                if int(self.player_sprite.blink_timer * 5) % 2 == 0:
                    self.player_sprite.alpha = 0
                else:
                    self.player_sprite.alpha = 255

        # Update enemies
        for e in self.scene["Enemies"]:
            e.update_path(self.player_sprite, self.astar_barrier_list, delta_time)
            e.follow_path(ENEMY_SPEED_IN_PIXELS, delta_time)
            e.update_animation()

        # Update Boss
        if self.boss_spawned:
            for boss in self.scene["Boss"]:
                boss.update_path(self.player_sprite, self.astar_barrier_list, delta_time)
                boss.follow_path(ENEMY_SPEED_IN_PIXELS, delta_time)
                boss.update_animation(delta_time)

            # When Boss dies
            if len(self.scene["Boss"]) == 0:
                self.boss_defeated = True
                win_view = WinView()
                self.window.show_view(win_view)
                return

        # Attack collision with enemies and boss
        for yarn_ball in self.yarn_ball_list:
            # Check collision of yarn ball with enemy
            enemies_shot = arcade.check_for_collision_with_list(yarn_ball, self.scene["Enemies"])
            for enemy in enemies_shot:
                enemy.take_damage()
                # Deal extra damage with powerup
                if self.powerup_active:
                    enemy.take_damage()
                    enemy.take_damage()
                yarn_ball.kill()
            boss_shot = arcade.check_for_collision_with_list(yarn_ball, self.scene["Boss"])
            for boss in boss_shot:
                boss.take_damage()
                # Deal a little extra damage with powerup
                if self.powerup_active:
                    boss.take_damage()
                self.boss_health.text = f"{boss.health:01d}/{boss.total_health:02d}"
                yarn_ball.kill()

    # WASD movement
    def on_key_press(self, key, modifiers):
        self.active_keys.add(key)
        self.update_movement()

        # shoot yarn ball
        if key == arcade.key.SPACE and not self.player_sprite.is_blinking:
            if (self.powerup_active):
                self.player_sprite.shoot_powerup()
            else:
                self.player_sprite.shoot()

        # Use powerup
        if key == arcade.key.Q and (not self.player_sprite.is_blinking) and (len(self.player_sprite.inventory) > 0):
            use_sfx = Sound(get_resource_path("assets/sfx/powerup.wav"))
            self.sfx_player = arcade.play_sound(use_sfx)
            # Remove oldest powerup from inventory
            del self.player_sprite.inventory[0]
            self.powerup_count.text = len(self.player_sprite.inventory)
            self.powerup_active = True

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

    def spawn_powerup(self):
        if random.random() < 0.005:
            spawn_x = random.randint(200, SCREEN_WIDTH - 300)
            spawn_y = random.randint(200, SCREEN_HEIGHT - 300)
            ball = GalaxyYarn(
                center_x=spawn_x,
                center_y=spawn_y,
                scale=0.5
            )
            self.scene["Powerups"].append(ball)

    def spawn_regular_enemies(self):
        if random.random() < self.enemy_spawn_rate:
            spawn_position = self.get_enemy_spawn_position()
            enemy = Fishhead(
                center_x=spawn_position[0],
                center_y=spawn_position[1],
                scale=0.75
            )
            self.scene["Enemies"].append(enemy)

    def get_enemy_spawn_position(self):
        # Each tile is 48x48 (originally 64x64 but scaled by 0.75)
        top_coords = {'x': 268, 'y': 0}
        bottom_coords = {'x': 268, 'y': SCREEN_HEIGHT - 1}
        left_coords = {'x': 0, 'y': 268}
        right_coords = {'x': SCREEN_WIDTH - SIDEBAR_WIDTH, 'y': 268}
        coords = [top_coords, bottom_coords, left_coords, right_coords]

        spawn_pos = random.randint(0, 3)  # Spawn position: top, bottom, left, right
        tile_num = random.randint(1, 4)  # Tile: one of 4 tiles
        position = coords[spawn_pos]  # Appropriate coordinates for the selected spawn position

        # Tile multiplier - get next 3 tiles beyond the topmost or leftmost one
        x_mult = 0
        y_mult = 0
        if spawn_pos < 2:
            x_mult = tile_num
        else:
            y_mult = tile_num

        spawn_x = position.get('x') + (48 * x_mult)
        spawn_y = position.get('y') + (48 * y_mult)
        return (spawn_x, spawn_y)