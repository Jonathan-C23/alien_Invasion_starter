"""
Bullet Module
Jonathan Carpenter

This module defines the Bullet class, a pygame Sprite representing the green
laser blasts fired by the player's TIE Fighter in the Star Wars-themed Alien
Invasion game. Bullets travel upward from the ship and are managed by the
Arsenal class.

date: 12/15/2025
"""


import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Bullet(Sprite):
    """
    A sprite class representing a single bullet (laser blast) fired from the player's ship.

    Bullets move straight upward at a constant speed and are drawn as scaled images.

    Attributes:
        screen (pygame.Surface): The main game screen surface.
        settings (Settings): Game settings containing bullet dimensions and speed.
        image (pygame.Surface): Scaled image of the green laser blast.
        rect (pygame.Rect): Rectangular area for positioning and collision detection.
        y (float): Precise vertical position for smooth movement.
    """


    def __init__(self, game: 'AlienInvasion'):
        """
        Create a new bullet at the ship's current position.

        Args:
            game (AlienInvasion): The main game instance, providing access to screen,
                                  settings, and the player's ship position.

        Returns:
            None
        """
        super().__init__()
        self.screen = game.screen
        self.settings = game.settings

        self.image = pygame.image.load(self.settings.bullet_file)
        self.image = pygame.transform.scale(self.image, (self.settings.bullet_w, self.settings.bullet_h))

        self.rect = self.image.get_rect()
        self.rect.midtop = game.ship.rect.midtop
        self.y = float(self.rect.y)
    
    def update(self):
        """
        Move the bullet upward by updating its position.

        Called once per frame by the sprite group.

        Returns:
            None
        """
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y
    
    def draw_bullet(self):
        """
        Draw the bullet (laser) to the screen at its current position.

        Returns:
            None
        """
        self.screen.blit(self.image, self.rect)