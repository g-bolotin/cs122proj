import arcade
from arcade import Sound
from src.music_player import MusicManager

from src import constants
from src import music_player
from src.views.base_view import BaseView
from src.utils import get_resource_path

class MainMenuView(BaseView):
    def __init__(self):
        super().__init__()

        self.cat_head = None
        self.fish_head = None
        self.music = None

    def on_show(self):
        MusicManager.stop_music()  # note: cannot stop music from previous view, will stop all music
        self.music = get_resource_path("assets/sfx/menu.wav")
        MusicManager.play_music(self.music, loop=True)

        # Set background color
        arcade.set_background_color((0, 204, 153))

        self.add_button("play", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 - 50, "Play")
        self.add_button("controls", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 - 125, "Controls")
        self.add_button("credits", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 - 200, "Credits")

        self.cat_head = arcade.Sprite(
            get_resource_path("assets/player/cat-head.png"),
            scale = 3
        )
        self.cat_head.center_x = constants.SCREEN_WIDTH / 4 - 50
        self.cat_head.center_y = constants.SCREEN_HEIGHT / 2 + 50
        self.cat_head.angle =-30

        self.fish_head = arcade.Sprite(
            get_resource_path("assets/enemies/fishhead/side-walk/fishhead-68-1.png"),
            scale = 3
        )
        self.fish_head.center_x = constants.SCREEN_WIDTH * 3 / 4 + 50
        self.fish_head.center_y = constants.SCREEN_HEIGHT / 2 + 50
        self.fish_head.angle = 30

    def on_draw(self):
        arcade.start_render()

        self.cat_head.draw()
        self.fish_head.draw()

        arcade.draw_text(
            constants.SCREEN_TITLE,
            constants.SCREEN_WIDTH / 2,
            constants.SCREEN_HEIGHT / 2 + 200,
            arcade.color.GOLD,
            font_size=100,
            anchor_x="center",
            font_name=constants.FONT_NAME
        )

        self.draw_buttons()

    def on_mouse_press(self, x, y, button, modifiers):
        # When mouse clicked, create instance of game view
        if self.buttons["play"]["is_hovering"]:
            from src.game_view import GameView
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

        elif self.buttons["controls"]["is_hovering"]:
            from src.views.controls_view import ControlsView
            controls_view = ControlsView()
            self.window.show_view(controls_view)

        elif self.buttons["credits"]["is_hovering"]:
            from src.views.credits_view import CreditsView
            credits_view = CreditsView()
            self.window.show_view(credits_view)
