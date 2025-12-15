"""
Ship Module
Jonathan Carpenter

This module defines the Ship class, representing the player-controlled TIE Fighter
in the Star Wars-themed Alien Invasion game. It handles ship movement, firing,
drawing, collision detection with aliens, and delegates bullet management to
the associated Arsenal instance.

date: 12/15/2025
"""


import pygame
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion
    from arsenal import Arsenal

class Ship:
    """
    Player-controlled ship (TIE Fighter) class.

    Manages the ship's position, movement along the bottom of the screen,
    firing lasers via the Arsenal, rendering, and basic collision detection
    with aliens.

    Attributes:
        game (AlienInvasion): Reference to the main game instance.
        settings (Settings): Game settings containing speeds and dimensions.
        screen (pygame.Surface): The main game screen surface.
        boundaries (pygame.Rect): Rect representing the screen boundaries.
        image (pygame.Surface): Scaled image of the TIE Fighter.
        rect (pygame.Rect): Rect for positioning and collision of the ship.
        x (float): Precise horizontal position for smooth movement.
        moving_right (bool): Flag indicating rightward movement.
        moving_left (bool): Flag indicating leftward movement.
        arsenal (Arsenal): Instance managing the ship's bullets/lasers.
    """

    def __init__(self, game: 'AlienInvasion', arsenal: 'Arsenal'):
        """
        Initialize the ship and set its starting position.

        Args:
            game (AlienInvasion): The main game instance, providing access to screen,
                                  settings, and other resources.
            arsenal (Arsenal): The Arsenal instance handling bullet creation and updates.

        Returns:
            None
        """
        self.game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = self.screen.get_rect()

        self.image = pygame.image.load(self.settings.ship_file)
        self.image = pygame.transform.scale(self.image, (self.settings.ship_w, self.settings.ship_h))

        self.rect = self.image.get_rect()
        self._center_ship()
        self.moving_right = False
        self.moving_left = False
        self.arsenal = arsenal

    def _center_ship(self):
        """
        Center the ship horizontally at the bottom of the screen.

        Also updates the precise floating-point x position.

        Returns:
            None
        """
        self.rect.midbottom = self.boundaries.midbottom
        self.x = float(self.rect.x)

    def update(self):
        """
        Update the ship's position and its arsenal based on movement flags.

        Called once per frame when the game is active.

        Returns:
            None
        """
        # updating the position of the ship
        self._update_ship_movement()
        self.arsenal.update_arsenal()

    def _update_ship_movement(self):
        """
        Update the ship's horizontal position based on movement flags and boundaries.

        Returns:
            None
        """
        if self.moving_right and self.rect.right < self.boundaries.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > self.boundaries.left:
            self.x -= self.settings.ship_speed

        self.rect.x = self.x

    def draw(self):
       """
        Draw the ship's bullets first (via arsenal) then the ship itself.

        Ensures bullets appear behind the ship visually if overlapping.

        Returns:
            None
        """
       self.arsenal.draw()
       self.screen.blit(self.image, self.rect)

    def fire(self):
        """
        Attempt to fire a bullet/laser.

        Delegates to the arsenal and returns whether a bullet was successfully fired.

        Returns:
            bool: True if a bullet was fired, False if limit reached.
        """
        return self.arsenal.fire_bullet()
    
    def check_collisions(self, other_group):
        """
        Check for collisions between the ship and sprites in another group (typically aliens).

        If a collision occurs, the ship is immediately recentered.

        Args:
            other_group (pygame.sprite.Group): Group of sprites to check against (e.g., alien fleet).

        Returns:
            bool: True if a collision occurred, False otherwise.
        """
        if pygame.sprite.spritecollide(self, other_group, False):
            self._center_ship()
            return True
        return False