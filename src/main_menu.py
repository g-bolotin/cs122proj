import arcade
from src import constants
from src.game_view import GameView
from src.credits_view import CreditsView

class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.play_button_x = 0
        self.play_button_y = 0
        self.play_button_width = 200
        self.play_button_height = 50
        self.is_hovering_play = False

        self.credits_button_x = 0
        self.credits_button_y = 0
        self.is_hovering_credits = False

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

        # Play button
        self.play_button_x = constants.SCREEN_WIDTH / 2
        self.play_button_y = constants.SCREEN_HEIGHT / 2 - 50
        self.draw_button(self.play_button_x, self.play_button_y, "Play", self.is_hovering_play)

        # Credits button
        self.credits_button_x = constants.SCREEN_WIDTH / 2
        self.credits_button_y = constants.SCREEN_HEIGHT / 2 - 150
        self.draw_button(self.credits_button_x, self.credits_button_y, "Credits", self.is_hovering_credits)

    def draw_button(self, x, y, text, is_hovering):
        button_color = (225, 225, 225) if is_hovering else arcade.color.WHITE
        arcade.draw_rectangle_filled(x, y, self.play_button_width, self.play_button_height, button_color)
        arcade.draw_text(
            text,
            x, y,
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

        self.is_hovering_credits = (
                self.credits_button_x - self.play_button_width / 2 <= x <= self.credits_button_x + self.play_button_width / 2 and
                self.credits_button_y - self.play_button_height / 2 <= y <= self.credits_button_y + self.play_button_height / 2
        )

    def on_mouse_press(self, x, y, button, modifiers):
        # When mouse clicked, create instance of game view
        if self.is_hovering_play:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

        elif self.is_hovering_credits:
            credits_view = CreditsView()
            self.window.show_view(credits_view)