import arcade
from src import constants

class BaseView(arcade.View):
    def draw_button(self, x, y, text, is_hovering):
        button_color = (225, 225, 225) if is_hovering else arcade.color.WHITE
        arcade.draw_rectangle_filled(x, y, constants.BUTTON_WIDTH, constants.BUTTON_HEIGHT, button_color)
        arcade.draw_text(
            text,
            x, y,
            arcade.color.BLACK,
            font_size=24,
            anchor_x="center",
            anchor_y="center",
            font_name=constants.FONT_NAME
        )
