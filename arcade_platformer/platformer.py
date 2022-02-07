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

from email.errors import BoundaryError
from tkinter import BOTTOM
import arcade
import pathlib

# Game constants
# Window dimensions
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "Arcade Platformer"

# Scaling constants
MAP_SCALING = 1.0

# Player constants
GRAVITY = 1.0
PLAYER_START_X = 65
PLAYER_START_Y = 256
PLAYER_MOVE_SPEED = 10
PLAYER_JUMP_SPEED = 20

# Viewport margins
# Defines how close the player has to be to scroll the viewport
LEFT_VIEWPORT_MARGIN = 50
RIGHT_VIEWPORT_MARGIN = 300
TOP_VIEWPORT_MARGIN = 150
BOTTOM_VIEWPORT_MARGIN = 150

# Assets path
ASSETS_PATH = pathlib.Path(__file__).resolve().parent.parent / "assets"

class Platformer(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

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
        # Get the current map based on the level
        map_name = f"platform_level_{self.level:02}.tmx"
        map_path = ASSETS_PATH / map_name

        # Match layers to names in arcade
        wall_layer = "Ground"
        coin_layer = "Collectibles"
        goal_layer = "Goal"
        background_layer = "Background"
        ladders_layer = "Ladders"

        # Load the current map
        game_map = arcade.tilemap.read_tmx(str(map_path))

        # Load the layers
        self.background = arcade.tilemap.process_layer(
            game_map, layer_name=background_layer, scaling=MAP_SCALING
        )
        self.goals = arcade.tilemap.process_layer(
            game_map, layer_name=goal_layer, scaling=MAP_SCALING
        )
        self.walls = arcade.tilemap.process_layer(
            game_map, layer_name=wall_layer, scaling=MAP_SCALING
        )
        self.ladders = arcade.tilemap.process_layer(
            game_map, layer_name=ladders_layer, scaling=MAP_SCALING
        )
        self.coins = arcade.tilemap.process_layer(
            game_map, layer_name=coin_layer, scaling=MAP_SCALING
        )

        # Set the background color
        background_color = arcade.color.FRESH_AIR
        if game_map.background_color:
            background_color = game_map.background_color
        arcade.set_background_color(background_color)

        # Find the map size to control viewport scrolling
        self.map_width = (game_map.map_size.width - 1) * game_map.tile_size.width

        # Create the player sprite if they're not already set up
        if not self.player:
            self.player = self.create_player_sprite()

        # Move the player sprite to the initial position
        self.player.center_x = PLAYER_START_X
        self.player.center_y = PLAYER_START_Y
        self.player.change_x = 0
        self.player.change_y = 0

        # Set up the viewport
        self.view_left = 0
        self.view_bottom = 0

        # Load the physics engine for this map
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            player_sprite=self.player,
            platforms=self.walls,
            gravity_constant=GRAVITY,
            ladders=self.ladders
        )
    
    def create_player_sprite(self) -> arcade.AnimatedWalkingSprite:
        """
        Creates the animated player sprite

        Returns:
           The properly set up player sprite
        """
        # Path to the textures for the image animation
        texture_path = ASSETS_PATH / "images" / "player"

        # Set up the appropriate textures
        walking_paths = [
            texture_path / f"alienGreen_walk{x}.png" for x in (1, 2)
        ]
        climbing_paths = [
            texture_path / f"alienGreen_climb{x}.png" for x in (1, 2)
        ]
        standing_path = texture_path / f"alienGreen_stand.png"

        # Load the textures
        walking_right_textures = [
            arcade.load_texture(texture) for texture in walking_paths
        ]
        walking_left_textures = [
            arcade.load_texture(texture, mirrored=True) for texture in walking_paths
        ]
        walking_up_textures = [
            arcade.load_texture(texture) for texture in climbing_paths
        ]
        walking_down_textures = [
            arcade.load_texture(texture, mirrored=True) for texture in climbing_paths
        ]
        standing_right_textures = [arcade.load_texture(standing_path)]
        standing_left_textures = [arcade.load_texture(standing_path, mirrored=True)]

        # Create the sprite
        player = arcade.AnimatedWalkingSprite()

        # Add the proper textures
        player.stand_left_textures = standing_left_textures
        player.stand_right_textures = standing_right_textures
        player.walk_left_textures = walking_left_textures
        player.walk_right_textures = walking_right_textures
        player.walk_up_textures = walking_up_textures
        player.walk_down_textures = walking_down_textures

        # Set the player defaults
        player.center_x = PLAYER_START_X
        player.center_y = PLAYER_START_Y
        player.state = arcade.FACE_RIGHT

        # Set the initial texture
        player.texture = player.stand_right_textures[0]

        return player

    def on_key_press(self, key: int, modifiers: int):
        """
        Processes key presses

        Args:
           key (int): Which key was pressed
           modifiers (int): Which modifiers were down at the time
        """
        # Check for player left or right movement
        if key in [arcade.key.LEFT, arcade.key.J]:
            self.player.change_x = -PLAYER_MOVE_SPEED
        elif key in [arcade.key.RIGHT, arcade.key.L]:
            self.player.change_x = PLAYER_MOVE_SPEED

        # Check if player can climb up or down
        elif key in [arcade.key.UP, arcade.key.I]:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = PLAYER_MOVE_SPEED
        elif key in [arcade.key.DOWN, arcade.key.K]:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = -PLAYER_MOVE_SPEED
        
        # Check if the player is able to jump
        elif key == arcade.key.SPACE:
            if self.physics_engine.can_jump():
                self.player.change_y = PLAYER_JUMP_SPEED
                # Play the jump sound
                arcade.play_sound(self.jump_sound)

    def on_key_release(self, key: int, modifiers: int):
        """
        Processes key releases

        Args:
           key (int): Which key was released
           modifiers (int): Which modifiers were down at the time
        """
        # Check for player left and right movement
        if key in [
            arcade.key.LEFT,
            arcade.key.J,
            arcade.key.RIGHT,
            arcade.key.L
        ]:
            self.player.change_x = 0

        # Check if player can climb up or down
        elif key in [
            arcade.key.UP,
            arcade.key.I,
            arcade.key.DOWN,
            arcade.key.K
        ]:
            if self.physics_engine.is_on_ladder():
                self.player.change_y = 0

    def scroll_viewport(self) -> None:
        """ Scroll the viewport when player is too close to edges. """
        # Scroll left
        # Find the current left boundary
        left_boundary = self.view_left + LEFT_VIEWPORT_MARGIN
        
        # Left of this boundary? If so, scroll left
        if self.player.left < left_boundary:
            self.view_left -= left_boundary - self.player.left
            # Don't scroll past left edge of map
            if self.view_left < 0:
                self.view_left = 0

        # Scroll right
        # Find the current right boundary
        right_boundary = self.view_left + SCREEN_WIDTH - RIGHT_VIEWPORT_MARGIN

        # Right of this boundary? If so, scroll right
        if self.player.right > right_boundary:
            self.view_left += self.player.right - right_boundary
            # Do not scroll past right edge of the map
            if self.view_left > self.map_width - SCREEN_WIDTH:
                self.view_left = self.map_width - SCREEN_WIDTH

        # Scroll up
        top_boundary = self.view_bottom + SCREEN_HEIGHT - TOP_VIEWPORT_MARGIN
        if self.player.top > top_boundary:
            self.view_bottom += self.player.top - top_boundary

        # Scroll down 
        bottom_boundary = self.view_bottom + BOTTOM_VIEWPORT_MARGIN
        if self.player.bottom < bottom_boundary:
            self.view_bottom -= bottom_boundary - self.player.bottom

        # Only scroll to integers so that we do not crop pixels unexpectedly
        self.view_bottom = int(self.view_bottom)
        self.view_left = int(self.view_left)

        # Do the scrolling
        arcade.set_viewport(
            left=self.view_left,
            right=SCREEN_WIDTH + self.view_left,
            bottom=self.view_bottom,
            top=SCREEN_HEIGHT + self.view_bottom
        )

    def on_update(self, delta_time: float):
        """
        Updates the position of game objects

        Args:
           delta_time (float): How much time since the last call
        """
        # Update the player animation
        self.player.update_animation(delta_time)

        # Update the player movement based on physics engine
        self.physics_engine.update()

        # Prevent player from walking off screen
        if self.player.left < 0:
            self.player.left = 0

        # Check if the player has picked up a coin
        coins_hit = arcade.check_for_collision_with_list(
            sprite=self.player, sprite_list=self.coins
        )

        for coin in coins_hit:
            # Add the coin value to the score
            self.score += int(coin.properties["point_value"])

            # Play the coin sound
            arcade.play_sound(self.coin_sound)

            # Remove the coin
            coin.remove_from_sprite_lists()

        # Check if the player has reached the goal
        goal_hit = arcade.check_for_collision_with_list(
            sprite=self.player, sprite_list=self.goals
        )

        if goal_hit:
            # Play the victory fanfare
            self.victory_sound.play()

            # Set up the next level
            self.level += 1
            self.setup()

        # Set the viewport scrolling if necessary
        self.scroll_viewport()

    def on_draw(self) -> None:
        arcade.start_render()

        # Draw all the sprites
        self.background.draw()
        self.walls.draw()
        self.coins.draw()
        self.goals.draw()
        self.ladders.draw()
        self.player.draw()

        # Draw the score on screen
        score_text = f"Score: {self.score}"

        # First, render a black-shaded background
        arcade.draw_text(
            score_text,
            start_x=10 + self.view_left,
            start_y=10 + self.view_bottom,
            color=arcade.csscolor.BLACK,
            font_size=40
        )

        # Then render the text in white slightly shifted
        arcade.draw_text(
            score_text,
            start_x=15 + self.view_left,
            start_y=15 + self.view_bottom,
            color=arcade.csscolor.WHITE,
            font_size=40
        )

if __name__ == '__main__':
    window = Platformer()
    window.setup()
    arcade.run()
