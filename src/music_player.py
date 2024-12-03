# # Global variables to control music across different menu views
# curr_playback = None
# curr_sfx = None

import arcade
class MusicManager:
    _player = None
    _current_sound = None

    @staticmethod
    def play_music(file_path, loop=False):
        # Stop current music if playing
        if MusicManager._player is not None:
            MusicManager.stop_music()

        # Load the new sound and create a player
        MusicManager._current_sound = arcade.Sound(file_path)
        MusicManager._player = MusicManager._current_sound.play(loop=loop)

    @staticmethod
    def stop_music():
        # Stop the current player and reset
        if MusicManager._player is not None:
            MusicManager._player.pause()  # Ensures immediate stop
            MusicManager._player.delete()

            MusicManager._player = None
            MusicManager._current_sound = None
