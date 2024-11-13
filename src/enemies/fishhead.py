import arcade
from src import constants
from arcade import FACE_RIGHT, FACE_LEFT, FACE_UP, FACE_DOWN
from src.enemies.enemy import Enemy

class Fishhead(Enemy):
    def __init__(self, center_x=0, center_y=0, scale=1):
        super().__init__(scale=scale, center_x=center_x, center_y=center_y)
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