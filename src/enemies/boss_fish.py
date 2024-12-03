import arcade
from src import constants
from arcade import FACE_RIGHT, FACE_LEFT, FACE_UP, FACE_DOWN

from src.constants import LEVEL_BORDER_SIZE, SIDEBAR_WIDTH
from src.enemies.enemy import Enemy, ENEMY_SPEED_IN_PIXELS
from src.utils import get_resource_path

MIN_DISTANCE = 192  # Distance player must move before enemy path is recalculated
CLEARED_SPAWN = 100  # Distance needed to move out of spawn area

class BossFish(Enemy):
    def __init__(self, center_x=0, center_y=0, scale=2):
        super().__init__(scale=scale, center_x=center_x, center_y=center_y)

        self.total_traveled_distance = 0
        self.straight_line_phase = True
        self.path_recalculation_timer = 0
        self.current_target_index = 0
        self.last_player_pos = None

        # For advancing frames in the animation by looping through textures
        self.cur_texture_index = 0
        self.time_counter = 0.0  # Time for controlling animation frame rate

        # Sprite size (boss is 2 times bigger)
        self.width = 68 * 2
        self.height = 68 * 2

        # Boss-specific attributes
        self.health = 50  # Increased health for the boss
        self.total_health = 50
        self.speed = ENEMY_SPEED_IN_PIXELS / 2  # Boss walks 2 times slower

        # Walking textures
        self.walk_left_textures = []
        self.walk_right_textures = []
        self.walk_up_textures = []
        self.walk_down_textures = []

        # Load walk left animation frames
        for i in range(1, 9):
            texture_name = f"bossfish-68-{i}.png"
            texture = arcade.load_texture(get_resource_path("assets/enemies/bossfish/side-walk/" + texture_name))
            self.walk_left_textures.append(texture)

        # Load walk right animation frames (flipped horizontally)
        for i in range(1, 9):
            texture_name = f"bossfish-68-{i}.png"
            texture = arcade.load_texture(
                get_resource_path("assets/enemies/bossfish/side-walk/" + texture_name), flipped_horizontally=True
            )
            self.walk_right_textures.append(texture)

        # Load walk down animation frames
        for i in range(1, 9):
            texture_name = f"bossfish-68-{i}.png"
            texture = arcade.load_texture(get_resource_path("assets/enemies/bossfish/side-walk/" + texture_name))
            self.walk_down_textures.append(texture)

        # Load walk up animation frames
        for i in range(1, 9):
            texture_name = f"bossfish-68-{i}.png"
            texture = arcade.load_texture(get_resource_path("assets/enemies/bossfish/side-walk/" + texture_name))
            self.walk_up_textures.append(texture)

        # List of all walk textures for easy access
        self.walk_textures = [
            self.walk_right_textures,
            self.walk_left_textures,
            self.walk_up_textures,
            self.walk_down_textures
        ]

        # Set default texture
        self.state = FACE_DOWN
        self.texture = self.walk_down_textures[0]

    def update_animation(self, delta_time: float = 1 / 60):
        self.time_counter += delta_time  # Time for controlling frame rate

        # Determine facing direction based on movement
        if self.change_x < 0:
            self.state = FACE_LEFT
        elif self.change_x > 0:
            self.state = FACE_RIGHT
        elif self.change_y > 0:
            self.state = FACE_UP
        elif self.change_y < 0:
            self.state = FACE_DOWN

        # Idle animation (if not moving)
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.walk_textures[self.state - 1][0]  # Show first frame
            self.time_counter = 0
            return

        # Walking animation
        animation_speed = 0.1  # Adjust as needed
        if self.time_counter > animation_speed:
            self.time_counter -= animation_speed
            self.cur_texture_index = (self.cur_texture_index + 1) % len(self.walk_textures[self.state - 1])
            self.texture = self.walk_textures[self.state - 1][self.cur_texture_index]

    def update(self):
        # Edge of screen collision logic
        super().update()

        # Adjust for boss size if needed
        if self.left < LEVEL_BORDER_SIZE:
            self.left = LEVEL_BORDER_SIZE
        elif self.right > constants.SCREEN_WIDTH - SIDEBAR_WIDTH - LEVEL_BORDER_SIZE:
            self.right = constants.SCREEN_WIDTH - SIDEBAR_WIDTH - LEVEL_BORDER_SIZE

        if self.bottom < LEVEL_BORDER_SIZE:
            self.bottom = LEVEL_BORDER_SIZE
        elif self.top > constants.SCREEN_HEIGHT - LEVEL_BORDER_SIZE:
            self.top = constants.SCREEN_HEIGHT - LEVEL_BORDER_SIZE

    def update_path(self, player_sprite, wall_list, delta_time):
        if self.straight_line_phase:
            # No need to update path until boss is out of spawn
            pass
        else:
            # Predict player's future position
            player_velocity_x = player_sprite.change_x
            player_velocity_y = player_sprite.change_y
            time_ahead = 0.5
            predicted_player_position = (
                player_sprite.center_x + player_velocity_x * time_ahead,
                player_sprite.center_y + player_velocity_y * time_ahead
            )

            # Check if path recalculation is needed
            if self.path_recalculation_timer <= 0 and (
                self.last_player_pos is None or (
                    (self.last_player_pos[0] - predicted_player_position[0]) ** 2 +
                    (self.last_player_pos[1] - predicted_player_position[1]) ** 2
                ) ** 0.5 > MIN_DISTANCE
            ):
                # Calculate new path
                new_path = arcade.astar_calculate_path(
                    start_point=(self.center_x, self.center_y),
                    end_point=predicted_player_position,
                    astar_barrier_list=wall_list,
                    diagonal_movement=False
                )
                # Update path and cooldown
                if new_path:
                    self.path = new_path
                    self.current_target_index = 0
                    self.last_player_pos = predicted_player_position
                self.path_recalculation_timer = 0.2  # Cooldown
            else:
                self.path_recalculation_timer -= delta_time

    def follow_path(self, speed, delta_time):
        # Boss walks 2 times slower
        adjusted_speed = speed / 2

        if (not self.path or self.current_target_index >= len(self.path)) and not self.straight_line_phase:
            self.change_x = 0
            self.change_y = 0
            return

        if self.straight_line_phase:
            # Move towards center until out of spawn area
            direction_x = 384 - self.center_x
            direction_y = 384 - self.center_y
            abs_dir_x = abs(direction_x)
            abs_dir_y = abs(direction_y)

            if abs_dir_x > abs_dir_y:
                self.change_x = adjusted_speed if direction_x > 0 else -adjusted_speed
                self.change_y = 0
            else:
                self.change_y = adjusted_speed if direction_y > 0 else -adjusted_speed
                self.change_x = 0

            self.center_x += self.change_x * delta_time
            self.center_y += self.change_y * delta_time

            self.total_traveled_distance += abs(self.change_x * delta_time) + abs(self.change_y * delta_time)

            if self.total_traveled_distance > CLEARED_SPAWN:
                self.straight_line_phase = False
        else:
            # Follow the calculated path
            target_x, target_y = self.path[self.current_target_index]
            diff_x = target_x - self.center_x
            diff_y = target_y - self.center_y
            distance = (diff_x ** 2 + diff_y ** 2) ** 0.5

            if distance < adjusted_speed * delta_time:
                self.center_x = target_x
                self.center_y = target_y
                self.current_target_index += 1
            else:
                self.change_x = (diff_x / distance) * adjusted_speed
                self.change_y = (diff_y / distance) * adjusted_speed
                self.center_x += self.change_x * delta_time
                self.center_y += self.change_y * delta_time
