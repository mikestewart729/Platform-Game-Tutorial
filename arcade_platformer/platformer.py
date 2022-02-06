"""
Arcade Platformer

Demonstrating the capabilities of arcade in a platformer game
Supporting the Arcade Platformer article
at https://realpython.com/platformer-python-arcade/

All game artwork from www.kenney.nl
Game sounds by Jon Fincher of RealPython
Level design by Mike Stewart
"""
# platformer.py

import arcade
import pathlib

# Game constants
# Window dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Arcade Platformer"

# Assets path
ASSETS_PATH = pathlib.Path(__file__).resolve().parent.parent / "assets"

class Platformer(arcade.Window):
    def __init__(self):
        super.__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

        # Lists to hold different sets of sprites
        self.coins = None
        self.background = None
        self.walls = None
        self.ladders = None
        self.goals = None
        self.enemies = None

        # One sprite for the player
        self.player = None

        # Platform game needs a physics engine
        self.physics_engine = None

        # Store the player's score
        self.score = 0

        # Store the level the player is on
        self.level = 1

        # Load game sounds
        self.coin_sound = arcade.load_sound(
            str(ASSETS_PATH / "sounds" / "coin.wav")
        )
        self.jump_sound = arcade.load_sound(
            str(ASSETS_PATH / "sounds" / "jump.wav")
        )
        self.victory_sound = arcade.load_sound(
            str(ASSETS_PATH / "sounds" / "victory.wav")
        )

    def setup(self):
        """ Sets up game for current level """
        pass

    def on_key_press(self, key: int, modifiers: int):
        """
        Processes key presses

        Args:
           key (int): Which key was pressed
           modifiers (int): Which modifiers were down at the time
        """
        pass

    def on_key_release(self, key: int, modifiers: int):
        """
        Processes key releases

        Args:
           key (int): Which key was released
           modifiers (int): Which modifiers were down at the time
        """
        pass

    def on_update(self, delta_time: float):
        """
        Updates the position of game objects

        Args:
           delta_time (float): How much time since the last call
        """

    def on_draw(self):
        pass

if __name__ == '__main__':
    window = Platformer()
    window.setup()
    arcade.run()
