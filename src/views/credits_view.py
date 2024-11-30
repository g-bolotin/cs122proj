import arcade
from src import constants
from src.views.base_view import BaseView

class CreditsView(BaseView):
    def __init__(self):
        super().__init__()

    def on_show(self):
        arcade.set_background_color((0, 204, 153))

        self.add_button("back", constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2 - 200, "Back")

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text(
            "Credits",
            constants.SCREEN_WIDTH / 2,
            constants.SCREEN_HEIGHT - 100,
            arcade.color.GOLD,
            font_size=50,
            anchor_x="center",
            font_name=constants.FONT_NAME
        )

        self.draw_buttons()

        # Credits
        content = [
            {"name": "Galit Bolotin", "role": "Programmer, Game Designer, Artist"},
            {"name": "Jeremy Chan", "role": "Programmer, Game Designer"}
        ]

        start_y = constants.SCREEN_HEIGHT / 2
        line_spacing = 40

        for i, entry in enumerate(content):
            y_position = start_y - i * line_spacing
            arcade.draw_text(
                f"{entry['name']}",
                constants.SCREEN_WIDTH / 2 - 100,
                y_position,
                arcade.color.WHITE,
                font_size=30,
                anchor_x="right",
                bold=True,
                font_name=constants.FONT_NAME
            )

            arcade.draw_text(
                entry["role"],
                constants.SCREEN_WIDTH / 2 + 10,
                y_position,
                arcade.color.WHITE,
                font_size=25,
                anchor_x="left",
                font_name=constants.FONT_NAME
            )

    def on_mouse_press(self, x, y, button, modifiers):
        if self.buttons["back"]["is_hovering"]:
            from src.views.main_menu import MainMenuView
            menu_view = MainMenuView()
            self.window.show_view(menu_view)
