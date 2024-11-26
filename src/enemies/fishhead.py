import arcade
from src import constants
from arcade import FACE_RIGHT, FACE_LEFT, FACE_UP, FACE_DOWN

from src.constants import LEVEL_BORDER_SIZE, SIDEBAR_WIDTH
from src.enemies.enemy import Enemy

MIN_DISTANCE = 2  # Small enough to consider the target reached

class Fishhead(Enemy):
    def __init__(self, center_x=0, center_y=0, scale=1):
        super().__init__(scale=scale, center_x=center_x, center_y=center_y)

        self.current_target_index = 0
        self.last_player_pos = None

        # For advancing frames in the animation by looping through textures
        self.cur_texture_index = 0
        self.texture_change_distance = 20
        self.last_texture_change_center_x = center_x
        self.last_texture_change_center_y = center_y

        # Sprite size
        self.width = 68
        self.height = 68

        # Load walk right animation frames
        for i in range(1, 9):
            texture_name = f"fishhead-68-{i}.png"
            texture = arcade.load_texture("../assets/enemies/fishhead/side-walk/" + texture_name)
            self.walk_left_textures.append(texture)

        # Load walk left animation frames
        for i in range(1, 9):
            texture_name = f"fishhead-68-{i}.png"
            texture = arcade.load_texture("../assets/enemies/fishhead/side-walk/" + texture_name, flipped_horizontally=True)
            self.walk_right_textures.append(texture)

        # Load walk down animation frames
        for i in range(1, 9):
            texture_name = f"fishhead-68-{i}.png"
            texture = arcade.load_texture("../assets/enemies/fishhead/side-walk/" + texture_name)
            self.walk_down_textures.append(texture)

        # Load walk up animation frames
        for i in range(1, 9):
            texture_name = f"fishhead-68-{i}.png"
            texture = arcade.load_texture("../assets/enemies/fishhead/side-walk/" + texture_name)
            self.walk_up_textures.append(texture)

        self.texture = self.walk_down_textures[0]  # set default idle to facing left

    def update_animation(self, delta_time: float = 1 / 60):
        self.time_counter += delta_time  # time for controlling frame rate

        # Detect movement start to reset time_counter
        if (self.change_x != 0 or self.change_y != 0) and self.time_counter == 0:
            self.time_counter = 0

        # Player facing direction based on movement
        # moving left on screen: face leftward
        if self.change_x < 0:
            self.texture = self.walk_left_textures[0]
            self.state = FACE_LEFT

        # moving right on screen: face rightward
        elif self.change_x > 0:
            self.texture = self.walk_right_textures[0]
            self.state = FACE_RIGHT

        # moving up on screen: face backward
        elif self.change_y > 0:
            self.texture = self.walk_up_textures[0]
            self.state = FACE_UP

        # moving down on screen: face forward
        elif self.change_y < 0:
            self.texture = self.walk_down_textures[0]
            self.state = FACE_DOWN

        # Idle animation -- for now, just the first frame of current walk animation
        if self.change_x == 0 and self.change_y == 0:
            self.texture = self.walk_textures[self.state - 1][self.cur_texture_index]  # states are 1-indexed
            self.time_counter = 0  # Reset time_counter to ensure smooth transition
            return

        # Walking animation
        animation_speed = 0.1  # higher value = slower animation frame rate
        if self.time_counter > animation_speed:
            self.time_counter -= animation_speed
            self.cur_texture_index += 1
            if self.cur_texture_index >= len(self.walk_textures[self.state - 1]):
                self.cur_texture_index = 0
        self.texture = self.walk_textures[self.state - 1][self.cur_texture_index]

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

    def update_path(self, player_sprite, wall_list, delta_time):

        player_position = (player_sprite.center_x, player_sprite.center_y)

        # Recalculate path if player has moved significantly
        # Uses Euclidean distance and compares it to the target position (slightly offset from actual player position)
        if self.last_player_pos is None or (
                (self.last_player_pos[0] - player_position[0]) ** 2 +
                (self.last_player_pos[1] - player_position[1]) ** 2
        ) ** 0.5 > MIN_DISTANCE:
            self.path = arcade.astar_calculate_path(
                start_point=(self.center_x, self.center_y),
                end_point=player_position,
                astar_barrier_list=wall_list,
                diagonal_movement=False
            )
            self.current_target_index = 0  # Reset to the start of the path
            self.last_player_pos = player_position

    def follow_path(self, speed, delta_time):
        if not self.path or self.current_target_index >= len(self.path):
            self.change_x = 0
            self.change_y = 0
            return  # No path or path complete

        # Get the current target waypoint
        target_x, target_y = self.path[self.current_target_index]

        # Calculate the difference between the current position and the target
        diff_x = target_x - self.center_x
        diff_y = target_y - self.center_y

        # Determine the movement direction
        distance = (diff_x ** 2 + diff_y ** 2) ** 0.5  # Pythagorean distance
        if distance < speed * delta_time:  # Close enough to the target
            self.center_x = target_x
            self.center_y = target_y
            self.current_target_index += 1  # Move to the next waypoint
        else:
            # Normalize the direction vector and scale by speed
            self.change_x = (diff_x / distance) * speed
            self.change_y = (diff_y / distance) * speed

            # Move by the computed amount
            self.center_x += self.change_x * delta_time
            self.center_y += self.change_y * delta_time