import arcade
from src import constants

class BaseView(arcade.View):
    def __init__(self):
        super().__init__()
        self.buttons = {}  # Dictionary to store buttons with their properties

    def add_button(self, key, x, y, text):
        # Add a button to the view
        self.buttons[key] = {
            "x": x,
            "y": y,
            "text": text,
            "is_hovering": False,
        }

    def draw_buttons(self):
        # Draw all buttons
        for button in self.buttons.values():
            button_color = (225, 225, 225) if button["is_hovering"] else arcade.color.WHITE
            arcade.draw_rectangle_filled(button["x"], button["y"], constants.BUTTON_WIDTH, constants.BUTTON_HEIGHT, button_color)
            arcade.draw_text(
                button["text"],
                button["x"], button["y"],
                arcade.color.BLACK,
                font_size=24,
                anchor_x="center",
                anchor_y="center",
                font_name=constants.FONT_NAME,
            )

    def on_mouse_motion(self, x, y, dx, dy):
        # Update hover state for all buttons
        for button in self.buttons.values():
            button["is_hovering"] = (
                button["x"] - constants.BUTTON_WIDTH / 2 <= x <= button["x"] + constants.BUTTON_WIDTH / 2 and
                button["y"] - constants.BUTTON_HEIGHT / 2 <= y <= button["y"] + constants.BUTTON_HEIGHT / 2
            )
