import arcade
import constants
from game_view import GameView


class MainMenuView(arcade.View):
    def on_show_view(self):
        # Set background color
        arcade.set_background_color(arcade.color.GRAY)

    def on_draw(self):
        arcade.start_render()
        arcade.draw_text(
            "TBD Game Name",
            constants.SCREEN_WIDTH / 2,
            constants.SCREEN_HEIGHT / 2 + 50,
            arcade.color.GOLD,
            font_size=50,
            anchor_x="center"
        )

        arcade.draw_text(
            "Click to Play",
            constants.SCREEN_WIDTH / 2,
            constants.SCREEN_HEIGHT / 2 - 50,
            arcade.color.WHITE,
            font_size=20,
            anchor_x="center"
        )

    def on_mouse_press(self, _x, _y, _button, _modifiers):
        # When mouse clicked, create instance of game view
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)