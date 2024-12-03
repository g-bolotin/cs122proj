import arcade
from src import constants
from src.music_player import MusicManager
from src.utils import get_resource_path
from src.views.base_view import BaseView

class WinView(BaseView):
    def __init__(self):
        super().__init__()
        self.music = None

    def on_show(self):
        MusicManager.stop_music()  # note: cannot stop music from previous view, will stop all music
        self.music = get_resource_path("assets/sfx/win.wav")
        MusicManager.play_music(self.music, loop=False)

        arcade.set_background_color((0, 204, 153))

        self.add_button("restart", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 - 50, "Restart")
        self.add_button("main_menu", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 - 125, "Main Menu")

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text(
            "YOU  WIN!",
            constants.SCREEN_WIDTH / 2,
            constants.SCREEN_HEIGHT / 2 + 150,
            arcade.color.GOLD,
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