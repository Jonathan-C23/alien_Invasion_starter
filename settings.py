"""
Settings Module
Jonathan Carpenter

This module defines the Settings class, which holds all static and dynamic
configuration values for the Star Wars-themed Alien Invasion game. It includes
screen dimensions, file paths for assets (images, sounds, fonts), colors, speeds,
difficulty scaling, and other game parameters.

date: 12/15/2025
"""

from pathlib import Path

class Settings:
    """
    Stores all settings for the Alien Invasion game.

    Contains static settings (screen size, asset paths, colors, etc.) set during
    initialization and dynamic settings (speeds, bullet limits, etc.) that are
    reset at the start of each game and increased as difficulty scales.

    Attributes:
        name (str): Window title and game name.
        screen_w (int): Screen width in pixels.
        screen_h (int): Screen height in pixels.
        FPS (int): Target frames per second.
        bg_file (Path): Path to background image.
        scores_file (Path): Path to JSON file storing the high score.
        ship_file (Path): Path to player ship image.
        bullet_file (Path): Path to bullet/laser image.
        alien_file (Path): Path to alien (enemy) image.
        font_file (Path): Path to custom Star Jedi font.
        life_image (Path): Path to icon used for remaining lives.
        laser_sound (Path): Path to laser firing sound effect.
        impact_sound (Path): Path to alien hit/explosion sound.
        music (Path): Path to background music (Imperial March).
    """
    def __init__(self):
        """
        Initialize static game settings, including asset paths and visual parameters.

        Returns:
            None
        """

        self.name: str = 'Alien Invasion'
        self.screen_w = 1000
        self.screen_h = 800
        self.FPS = 60
        self.bg_file = Path.cwd() / 'Assets' / 'images' / 'StarBackground.png'
        """
        Star Wars stars background
        StarBackground.png
        https://starwars.fandom.com/wiki/Star
        """
        self.difficulty_scale = 1.1
        self.scores_file = Path.cwd() / 'Assets' / 'file' / 'scores.json'
        
        self.ship_file = Path.cwd() / 'Assets' / 'images' / 'TieFighter.png'
        """
        Tie Fighter
        TieFighter.png
        https://www.nicepng.com/ourpic/u2q8q8q8o0t4y3w7_tie-fighter-tie-fighter-pixel-png/
        """
        self.ship_w = 80
        self.ship_h = 60

        self.bullet_file = Path.cwd() / 'Assets' / 'images' / 'greenLaserBlast.png'
        """
        Green laser
        greenLaserBlast.png
        beams.png
        """
        self.laser_sound = Path.cwd() / 'Assets' / 'sound' / 'laser2.mp3'
        """
        Star Wars Tie fighter blaster sound effect
        laser2.mp3
        https://www.youtube.com/watch?v=UfFiQ-gtLv4
        """
        self.impact_sound = Path.cwd() / 'Assets' / 'sound' / 'impactSound2.mp3'
        """
        Star Wars Explosions
        impactSound2.mp3
        https://www.youtube.com/watch?v=PpRVyBbBD5k
        """

        self.alien_file = Path.cwd() / 'Assets' / 'images' / 'xwing.png'
        """
        Red X Wing
        xwing.png
        https://www.pngfind.com/mpng/hJmJbhb_x-wing-red-x-wing-pixel-art-png/
        """
        self.alien_w = 55
        self.alien_h = 55
        self.fleet_direction = 1

        self.button_w = 200
        self.button_h = 50
        self.button_color = (0,135,50)
        
        self.text_color = (255, 255, 255)
        self.button_font_size = 48
        self.HUD_font_size = 20
        self.font_file = Path.cwd() / 'Assets' / 'Fonts' / 'Starjedi' / 'Starjedi.ttf'
        """
        Star Jedi Font
        Starjedi.ttf
        https://www.dafont.com/star-jedi.font
        """

        self.life_image = Path.cwd() / 'Assets' / 'images' / 'life.png'
        """
        First Order Stormtrooper
        life.png
        https://www.reddit.com/r/PixelArt/comments/wn1mvc/first_order_stormtrooper/
        """
        self.life_w = 40
        self.life_h = 40

        self.music = Path.cwd() / 'Assets' / 'sound' / 'music.mp3'
        """
        Imperial March Theme
        music.mp3
        https://www.youtube.com/watch?v=-bzWSJG93P8&list=RD-bzWSJG93P8&start_radio=1
        """

    def initialize_dynamic_settings(self):
        """
        Initialize or reset settings that can change during gameplay.

        Sets starting values for speeds and limits. Called at the beginning
        of each new game.

        Returns:
            None
        """
        self.ship_speed = 5
        self.starting_ship_count = 2

        self.bullet_speed = 7
        self.bullet_w = 25
        self.bullet_h = 80
        self.bullet_amount = 5

        self.fleet_speed = 4
        self.fleet_drop_speed = 50
        self.alien_points = 50

    def increase_difficulty(self):
        """
        Increase game difficulty by scaling speeds.

        Multiplies ship, bullet, and fleet speeds by the difficulty scale factor.
        Called each time a level is completed.

        Returns:
            None
        """
        self.ship_speed *= self.difficulty_scale
        self.bullet_speed *= self.difficulty_scale
        self.fleet_speed *= self.difficulty_scale