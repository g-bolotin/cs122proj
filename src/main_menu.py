import arcade
from src import constants
from src.game_view import GameView


class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.play_button_x = 0
        self.play_button_y = 0
        self.play_button_width = 0
        self.play_button_height = 0
        self.is_hovering_play = False

    def on_show_view(self):
        # Set background color
        arcade.set_background_color((0, 204, 153))

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text(
            constants.SCREEN_TITLE,
            constants.SCREEN_WIDTH / 2,
            constants.SCREEN_HEIGHT / 2 + 50,
            arcade.color.GOLD,
            font_size=100,
            anchor_x="center",
            font_name=constants.FONT_NAME
        )

        self.play_button_x = constants.SCREEN_WIDTH / 2
        self.play_button_y = constants.SCREEN_HEIGHT / 2 - 50
        self.play_button_width = 200
        self.play_button_height = 50

        if self.is_hovering_play:
            button_color = (225, 225, 225)
        else:
            button_color = arcade.color.WHITE

        arcade.draw_rectangle_filled(
            self.play_button_x,
            self.play_button_y,
            self.play_button_width,
            self.play_button_height,
            button_color
        )

        arcade.draw_text(
            "Play",
            self.play_button_x,
            self.play_button_y,
            arcade.color.BLACK,
            font_size=24,
            anchor_x="center",
            anchor_y="center",
            font_name=constants.FONT_NAME
        )

    def on_mouse_motion(self, x, y, dx, dy):
        self.is_hovering_play = (
            self.play_button_x - self.play_button_width / 2 <= x <= self.play_button_x + self.play_button_width / 2 and
            self.play_button_y - self.play_button_height / 2 <= y <= self.play_button_y + self.play_button_height / 2
        )

    def on_mouse_press(self, x, y, button, modifiers):
        # When mouse clicked, create instance of game view
        if (self.play_button_x - self.play_button_width / 2 <= x <= self.play_button_x + self.play_button_width / 2 and
            self.play_button_y - self.play_button_height / 2 <= y <= self.play_button_y + self.play_button_height / 2):
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)