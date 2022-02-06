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

class Platformer(arcade.Window):
    def __init__(self):
        pass

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
