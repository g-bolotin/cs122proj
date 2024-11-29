import arcade
from src import constants

class CreditsView(arcade.View):
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
            "Credits",
            constants.SCREEN_WIDTH / 2,
            constants.SCREEN_HEIGHT - 100,
            arcade.color.GOLD,
            font_size=50,
            anchor_x="center",
            font_name=constants.FONT_NAME
        )

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

        self.back_button_x = constants.SCREEN_WIDTH / 2
        self.back_button_y = 100
        self.draw_button(self.back_button_x, self.back_button_y, "Back", self.is_hovering_back)

    def draw_button(self, x, y, text, is_hovering):
        button_color = (225, 225, 225) if is_hovering else arcade.color.WHITE
        arcade.draw_rectangle_filled(x, y, self.back_button_width, self.back_button_height, button_color)
        arcade.draw_text(
            text,
            x,
            y,
            arcade.color.BLACK,
            font_size=24,
            anchor_x="center",
            anchor_y="center",
            font_name=constants.FONT_NAME
        )

    def on_mouse_motion(self, x, y, dx, dy):
        self.is_hovering_back = (
                self.back_button_x - self.back_button_width / 2 <= x <= self.back_button_x + self.back_button_width / 2 and
                self.back_button_y - self.back_button_height / 2 <= y <= self.back_button_y + self.back_button_height / 2
        )

    def on_mouse_press(self, x, y, button, modifiers):
        if self.is_hovering_back:
            from src.main_menu import MainMenuView
            menu_view = MainMenuView()
            self.window.show_view(menu_view)
