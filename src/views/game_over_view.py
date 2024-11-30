import arcade

from src import constants
from src.views.base_view import BaseView

class GameOverView(BaseView):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color(arcade.color.BLACK)

        self.add_button("restart", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 - 50, "Restart")
        self.add_button("main_menu", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 - 125, "Main Menu")

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text(
            "GAME  OVER",
            constants.SCREEN_WIDTH / 2,
            constants.SCREEN_HEIGHT / 2 + 150,
            arcade.color.RED,
            font_size=100,
            anchor_x="center",
            font_name=constants.FONT_NAME
        )

        self.draw_buttons()

    def on_mouse_press(self, x, y, button, modifiers):
        if self.buttons["restart"]["is_hovering"]:
            from src.game_view import GameView
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)

        elif self.buttons["main_menu"]["is_hovering"]:
            from src.views.main_menu import MainMenuView
            menu_view = MainMenuView()
            self.window.show_view(menu_view)