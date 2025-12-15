"""
Alien Module
Jonathan Carpenter

This module defines the Alien class, a pygame Sprite representing a single
enemy X-Wing fighter in the Star Wars-themed Alien Invasion game. Aliens are
managed collectively by the AlienFleet class, which controls their movement
direction and speed. Each alien moves horizontally and draws itself on the screen.

date: 12/15/2025
"""


import pygame
from pygame.sprite import Sprite
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_fleet import AlienFleet

class Alien(Sprite):
    """
    A single enemy alien (X-Wing) sprite.

    Represents one enemy ship in the fleet. Handles its own positioning,
    horizontal movement based on fleet direction and speed, edge detection,
    and rendering.

    Attributes:
        fleet (AlienFleet): Reference to the managing AlienFleet instance.
        screen (pygame.Surface): The main game screen surface.
        boundaries (pygame.Rect): Rect representing the screen boundaries.
        settings (Settings): Game settings containing dimensions and fleet speeds.
        image (pygame.Surface): Scaled image of the X-Wing.
        rect (pygame.Rect): Rect for positioning and collision detection.
        x (float): Precise horizontal position for smooth movement.
        y (float): Precise vertical position (used when dropping).
    """

    def __init__(self, fleet: 'AlienFleet', x: float, y: float):
        """
        Initialize the alien and place it at the specified coordinates.

        Args:
            fleet (AlienFleet): The AlienFleet instance managing this alien.
            x (float): Initial horizontal position in pixels.
            y (float): Initial vertical position in pixels.

        Returns:
            None
        """
        super().__init__()
        self.fleet = fleet
        self.screen = fleet.game.screen
        self.boundaries = fleet.game.screen.get_rect()
        self.settings = fleet.game.settings

        self.image = pygame.image.load(self.settings.alien_file)
        self.image = pygame.transform.scale(self.image, (self.settings.alien_w, self.settings.alien_h))

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.y = float(self.rect.y)
        self.x = float(self.rect.x)
        
    
    def update(self):
        """
        Update the alien's horizontal position based on fleet speed and direction.

        Movement is uniform across the fleet. Vertical drops are handled by the fleet.

        Returns:
            None
        """
        temp_speed = self.settings.fleet_speed
        
        # if self.check_edges():
            # self.settings.fleet_direction *= -1
            # self.y += self.settings.fleet_drop_speed

        self. x += temp_speed * self.fleet.fleet_direction
        self.rect.x = self.x
        self.rect.y = self.y

    def check_edges(self):
        """
        Determine if the alien has reached either horizontal edge of the screen.

        Used by the fleet to decide when to reverse direction and drop.

        Returns:
            bool: True if the alien is at or beyond the left or right screen edge.
        """
        return (self.rect.right >= self.boundaries.right or self.rect.left <= self.boundaries.left)
    

    def draw_alien(self):
        """
        Draw the alien (X-Wing) to the screen at its current position.

        Returns:
            None
        """
        self.screen.blit(self.image, self.rect)
