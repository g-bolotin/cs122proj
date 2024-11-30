import arcade
from src import constants
from src.views.base_view import BaseView

class MainMenuView(BaseView):
    def __init__(self):
        super().__init__()
        self.play_button_x = 0
        self.play_button_y = 0
        self.is_hovering_play = False

        self.credits_button_x = 0
        self.credits_button_y = 0
        self.is_hovering_credits = False

        self.controls_button_x = 0
        self.controls_button_y = 0
        self.is_hovering_controls = False

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

        # Controls button
        self.controls_button_x = constants.SCREEN_WIDTH / 2
        self.controls_button_y = constants.SCREEN_HEIGHT / 2 - 125
        self.draw_button(self.controls_button_x, self.controls_button_y, "Controls", self.is_hovering_controls)

        # Credits button
        self.credits_button_x = constants.SCREEN_WIDTH / 2
        self.credits_button_y = constants.SCREEN_HEIGHT / 2 - 200
        self.draw_button(self.credits_button_x, self.credits_button_y, "Credits", self.is_hovering_credits)

    def on_mouse_motion(self, x, y, dx, dy):
        self.is_hovering_play = (
            self.play_button_x - constants.BUTTON_WIDTH / 2 <= x <= self.play_button_x + constants.BUTTON_WIDTH / 2 and
            self.play_button_y - constants.BUTTON_HEIGHT / 2 <= y <= self.play_button_y + constants.BUTTON_HEIGHT / 2
        )

        self.is_hovering_credits = (
            self.credits_button_x - constants.BUTTON_WIDTH / 2 <= x <= self.credits_button_x + constants.BUTTON_WIDTH / 2 and
            self.credits_button_y - constants.BUTTON_HEIGHT / 2 <= y <= self.credits_button_y + constants.BUTTON_HEIGHT / 2
        )

        self.is_hovering_controls = (
                self.controls_button_x - constants.BUTTON_WIDTH / 2 <= x <= self.controls_button_x + constants.BUTTON_WIDTH / 2 and
                self.controls_button_y - constants.BUTTON_HEIGHT / 2 <= y <= self.controls_button_y + constants.BUTTON_HEIGHT / 2
        )

    def on_mouse_press(self, x, y, button, modifiers):
        # When mouse clicked, create instance of game view
        if self.is_hovering_play:
            from src.game_view import GameView
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

        elif self.is_hovering_credits:
            from src.views.credits_view import CreditsView
            credits_view = CreditsView()
            self.window.show_view(credits_view)

        elif self.is_hovering_controls:
            from src.views.controls_view import ControlsView
            controls_view = ControlsView()
            self.window.show_view(controls_view)