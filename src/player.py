import arcade
from src import constants
from arcade import FACE_RIGHT, FACE_LEFT, FACE_UP, FACE_DOWN

class Player(arcade.Sprite):
    def __init__(self, center_x=0, center_y=0, scale=1):
        super().__init__(scale=scale, center_x=center_x, center_y=center_y)

        self.state = FACE_DOWN   # player directionality
        self.time_counter = 0.0  # for controlling animation frame rate

        # Walking textures
        self.stand_left_textures = []
        self.stand_right_textures = []
        self.walk_left_textures = []
        self.walk_right_textures = []
        self.walk_up_textures = []
        self.walk_down_textures = []

        # List of all walk texture categories -- allows access to correct walking direction by player direction state
        self.walk_textures = [
            self.walk_right_textures,
            self.walk_left_textures,
            self.walk_up_textures,
            self.walk_down_textures
        ]

        # For advancing frames in the animation by looping through textures
        self.cur_texture_index = 0
        self.texture_change_distance = 20
        self.last_texture_change_center_x = center_x
        self.last_texture_change_center_y = center_y

        # Player sprite size -- necessary for collision detection
        self.width = 64
        self.height = 64

        # Load walk right animation frames
        for i in range(1, 5):
            texture_name = f"cat-right-64-{i}.png"
            texture = arcade.load_texture("../assets/player/side-walk/" + texture_name)
            print(f"walk right: frame {i}")
            if texture:
                print("loaded texture: " + texture_name)
            self.walk_right_textures.append(texture)

        # Load walk left animation frames
        for i in range(1, 5):
            texture_name = f"cat-right-64-{i}.png"
            texture = arcade.load_texture("../assets/player/side-walk/" + texture_name, flipped_horizontally=True)
            print(f"walk left: frame {i}")
            if texture:
                print("loaded texture: " + texture_name)
            self.walk_left_textures.append(texture)

        # Load walk down animation frames
        for i in range(1, 5):
            texture_name = f"cat-front-64-{i}.png"
            texture = arcade.load_texture("../assets/player/front-walk/" + texture_name)
            print(f"walk down: frame {i}")
            if texture:
                print("loaded texture: " + texture_name)
            self.walk_down_textures.append(texture)

        # Load walk up animation frames
        for i in range(1, 5):
            texture_name = f"cat-back-64-{i}.png"
            texture = arcade.load_texture("../assets/player/back-walk/" + texture_name)
            print(f"walk up: frame {i}")
            if texture:
                print("loaded texture: " + texture_name)
            self.walk_up_textures.append(texture)

        self.texture = self.walk_down_textures[0]  # set default idle to facing down

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
            self.texture = self.walk_textures[self.state-1][self.cur_texture_index]  # states are 1-indexed
            self.time_counter = 0  # Reset time_counter to ensure smooth transition
            return

        # Walking animation
        animation_speed = 0.1  # higher value = slower animation frame rate
        if self.time_counter > animation_speed:
            self.time_counter -= animation_speed
            self.cur_texture_index += 1
            if self.cur_texture_index >= len(self.walk_textures[self.state - 1]):
                self.cur_texture_index = 0
        self.texture = self.walk_textures[self.state-1][self.cur_texture_index]

    def update(self):

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