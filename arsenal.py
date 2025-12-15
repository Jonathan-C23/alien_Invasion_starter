"""
Arsenal Module
Jonathan Carpenter

This module defines the Arsenal class, which manages the collection of bullets
(green laser blasts) fired by the player's TIE Fighter in the Star Wars-themed
Alien Invasion game. It limits the number of simultaneous bullets, updates their
positions, removes off-screen bullets, draws them, and handles firing new ones.

date: 12/15/2025
"""


import pygame
from bullet import Bullet
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    


class Arsenal:
    """
    Manages the player's bullets (lasers).

    Uses a pygame sprite Group to store and update all active Bullet instances.
    Enforces a maximum number of on-screen bullets and removes those that travel
    off the top of the screen.

    Attributes:
        game (AlienInvasion): Reference to the main game instance.
        settings (Settings): Game settings containing the bullet limit.
        arsenal (pygame.sprite.Group): Group containing all active Bullet sprites.
    """


    def __init__(self, game: 'AlienInvasion'):
        """
        Initialize the arsenal and create an empty bullet group.

        Args:
            game (AlienInvasion): The main game instance, providing access to settings.

        Returns:
            None
        """
        self.game = game
        self.settings = game.settings
        self.arsenal = pygame.sprite.Group()

    def update_arsenal(self):
        """
        Update positions of all bullets and remove those that have left the screen.

        Called once per frame when the game is active.

        Returns:
            None
        """
        self.arsenal.update()
        self._remove_bullets_offscreen()

    def _remove_bullets_offscreen(self):
        """
        Remove bullets that have moved off the top edge of the screen.

        Iterates over a copy of the group to safely remove items during iteration.

        Returns:
            None
        """
        for bullet in self.arsenal.copy():
            if bullet.rect.bottom <= 0:
                self.arsenal.remove(bullet)
    
    def draw(self):
        """
        Draw all active bullets to the screen.

        Returns:
            None
        """
        for bullet in self.arsenal:
            bullet.draw_bullet()
    
    def fire_bullet(self):
        """
        Fire a new bullet if the maximum on-screen limit has not been reached.

        Creates a new Bullet instance positioned at the ship's current location
        and adds it to the group.

        Returns:
            bool: True if a bullet was fired, False if the limit was reached.
        """
        if len(self.arsenal) < self.settings.bullet_amount:
            new_bullet = Bullet(self.game)
            self.arsenal.add(new_bullet)
            return True
        return False