import arcade
from src import constants
from src.views.main_menu import MainMenuView

def main():
    # Create game window with dimensions and title
    window = arcade.Window(constants.SCREEN_WIDTH, constants.SCREEN_HEIGHT, constants.SCREEN_TITLE)

    # create and show  main menu
    menu_view = MainMenuView()
    window.show_view(menu_view)

    arcade.run()

if __name__ == '__main__':
    main()