import arcade
from src import constants
from src.views.base_view import BaseView

class ControlsView(BaseView):
    def __init__(self):
        super().__init__()
        self.back_button_x = 0
        self.back_button_y = 0
        self.back_button_width = 200
        self.back_button_height = 50
        self.is_hovering_back = False

    def on_show_view(self):
        arcade.set_background_color((0, 204, 153))

    def on_draw(self):
        arcade.start_render()

        arcade.draw_text(
            "Controls",
            constants.SCREEN_WIDTH / 2,
            constants.SCREEN_HEIGHT - 100,
            arcade.color.GOLD,
            font_size=50,
            anchor_x="center",
            font_name=constants.FONT_NAME
        )

        # Credits
        content = [
            {"control": "Move Up", "key": "W"},
            {"control": "Move Down", "key": "S"},
            {"control": "Move Left", "key": "A"},
            {"control": "Move Right", "key": "D"},
            {"control": "Shoot", "key": "Space"}
        ]

        start_y = constants.SCREEN_HEIGHT / 2 + 100
        line_spacing = 40

        for i, entry in enumerate(content):
            y_position = start_y - i * line_spacing
            arcade.draw_text(
                f"{entry['control']}",
                constants.SCREEN_WIDTH / 2 - 50,
                y_position,
                arcade.color.WHITE,
                font_size=25,
                anchor_x="right",
                bold=True,
                font_name=constants.FONT_NAME
            )

            arcade.draw_text(
                entry["key"],
                constants.SCREEN_WIDTH / 2 + 50,
                y_position,
                arcade.color.WHITE,
                font_size=25,
                anchor_x="left",
                font_name=constants.FONT_NAME
            )

        self.back_button_x = constants.SCREEN_WIDTH / 2
        self.back_button_y = 100
        self.draw_button(self.back_button_x, self.back_button_y, "Back", self.is_hovering_back)

    def on_mouse_motion(self, x, y, dx, dy):
        self.is_hovering_back = (
                self.back_button_x - self.back_button_width / 2 <= x <= self.back_button_x + self.back_button_width / 2 and
                self.back_button_y - self.back_button_height / 2 <= y <= self.back_button_y + self.back_button_height / 2
        )

    def on_mouse_press(self, x, y, button, modifiers):
        if self.is_hovering_back:
            from src.views.main_menu import MainMenuView
            menu_view = MainMenuView()
            self.window.show_view(menu_view)
