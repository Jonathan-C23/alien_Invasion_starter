"""
AlienFleet Module
Jonathan Carpenter

This module defines the AlienFleet class, which manages a group of Alien (X-Wing)
sprites in the Star Wars-themed Alien Invasion game. It creates an X-shaped
fleet formation, handles fleet movement (side-to-side with drops at edges),
updates all aliens, draws them, checks collisions with bullets, and detects
when the fleet is fully destroyed or reaches the bottom of the screen.

date: 12/15/2025
"""


import pygame
from alien import Alien
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class AlienFleet:
    """
    Manages the entire fleet of enemy aliens (X-Wings).

    Responsible for creating an X-shaped formation centered on the screen,
    moving the fleet as a cohesive unit, detecting edge collisions, dropping
    the fleet downward, and handling collisions with player bullets.

    Attributes:
        game (AlienInvasion): Reference to the main game instance.
        settings (Settings): Game settings containing dimensions and speeds.
        fleet (pygame.sprite.Group): Group containing all active Alien instances.
        fleet_direction (int): 1 for right, -1 for left movement.
        fleet_drop_speed (float): Vertical distance the fleet drops when hitting an edge.
    """

    def __init__(self, game: 'AlienInvasion'):
        """
        Initialize the alien fleet and create the initial X-shaped formation.

        Args:
            game (AlienInvasion): The main game instance, providing access to settings.

        Returns:
            None
        """
        self.game = game
        self.settings = game.settings
        self.fleet = pygame.sprite.Group()
        self.fleet_direction = self.settings.fleet_direction
        self.fleet_drop_speed = self.settings.fleet_drop_speed

        self.create_fleet()

    def create_fleet(self):
        """
        Create the full X-shaped alien fleet centered on the upper half of the screen.

        Calculates fleet size based on screen and alien dimensions, then positions
        aliens along the main and anti-diagonals to form an "X".

        Returns:
            None
        """
        alien_w = self.settings.alien_w
        alien_h = self.settings.alien_h
        screen_w = self.settings.screen_w
        screen_h = self.settings.screen_h

        fleet_w, fleet_h = self.calculate_fleet_size(alien_w, screen_w, alien_h, screen_h)

        half_screen = self.settings.screen_h//2
        fleet_horizontal_space = fleet_w * alien_w
        fleet_verticle_space = fleet_h * alien_h
        x_offset = int((screen_w-fleet_horizontal_space)//2)
        y_offset = int((half_screen-fleet_verticle_space)//2)

        self._create_x_fleet(alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset)

    def _create_x_fleet(self, alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset):
        """
        Place aliens only on the main diagonal and anti-diagonal to form an "X".

        Args:
            alien_w (int): Width of a single alien.
            alien_h (int): Height of a single alien.
            fleet_w (int): Number of columns in the fleet grid.
            fleet_h (int): Number of rows in the fleet grid.
            x_offset (int): Horizontal offset to center the fleet.
            y_offset (int): Vertical offset to position the fleet.

        Returns:
            None
        """
        for row in range(fleet_h):
            for col in range(fleet_w):
                # Place alien on main diagonal or anti-diagonal
                if col == row or col == (fleet_w - 1 - row):
                    current_x = col * alien_w + x_offset
                    current_y = row * alien_h + y_offset
                    self._create_alien(current_x, current_y)

    def _create_rectangle_fleet(self, alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset):
        """
        Alternative fleet creation method for a rectangular grid (currently unused).

        Skips every other position for a checkerboard-like pattern.

        Returns:
            None
        """
        for row in range(fleet_h):
            for col in range (fleet_w):
                current_x = alien_w * col + x_offset
                current_y = alien_h * row + y_offset
                if col % 2 == 0 or row % 2 == 0:
                    continue
                self._create_alien(current_x, current_y)

    def calculate_fleet_size(self, alien_w, screen_w, alien_h, screen_h):
        """
        Calculate a square, odd-sized fleet dimension that fits safely within the screen.

        Aims for approximately half the available space, ensures odd size for symmetry,
        and enforces a minimum size of 7.

        Args:
            alien_w (int): Width of one alien.
            screen_w (int): Screen width.
            alien_h (int): Height of one alien.
            screen_h (int): Screen height.

        Returns:
            tuple[int, int]: Width and height (in alien count) of the fleet grid.
        """
        # Target fraction of the screen to occupy (adjust if you want exactly 2/3 or less/more)
        fraction = 0.5  # Slightly under 2/3 to safely avoid touching edges on most resolutions

        
        max_fleet_w = screen_w // alien_w
        max_fleet_h = screen_h // alien_h

        target_w = int(max_fleet_w * fraction)
        target_h = int(max_fleet_h * fraction)

        # Odd for symmetry
        if target_w % 2 == 0:
            target_w -= 1
        if target_h % 2 == 0:
            target_h -= 1

        fleet_w = target_w
        fleet_h = target_h

        
        size = min(fleet_w, fleet_h)
        if size % 2 == 0:
            size -= 1
        size = max(7, size)
        fleet_w = fleet_h = size

        return fleet_w, fleet_h

    def _create_alien(self, current_x: int, current_y: int):
        """
        Create and add a single Alien instance at the specified pixel coordinates.

        Args:
            current_x (int): Horizontal position of the alien.
            current_y (int): Vertical position of the alien.

        Returns:
            None
        """
        new_alien = Alien(self, current_x, current_y)
        self.fleet.add(new_alien)

    def _check_fleet_edges(self):
        """
        Check if any alien has reached a horizontal edge; if so, reverse direction and drop.

        Returns:
            None
        """
        alien: Alien
        for alien in self.fleet:
            if alien.check_edges():
                self._drop_alien_fleet()
                self.fleet_direction *= -1
                break

    def _drop_alien_fleet(self):
        """
        Drop all aliens vertically by the fleet drop speed.

        Returns:
            None
        """
        for alien in self.fleet:
            alien.y += self.fleet_drop_speed

    def update_fleet(self):
        """
        Update the position of the entire fleet (edge checking + individual updates).

        Called once per frame when the game is active.

        Returns:
            None
        """
        self._check_fleet_edges()
        self.fleet.update()

    def draw(self):
        """
        Draw all aliens in the fleet to the screen.

        Returns:
            None
        """
        alien: 'Alien'
        for alien in self.fleet:
            alien.draw_alien()

    def check_collisions(self, other_group):
        """
        Check for collisions between aliens and another sprite group (typically bullets).

        Removes both the alien and the bullet on collision.

        Args:
            other_group (pygame.sprite.Group): Group to check against (usually bullets).

        Returns:
            dict: Collision dictionary from pygame.sprite.groupcollide.
        """
        return pygame.sprite.groupcollide(self.fleet, other_group, True, True)

    def check_fleet_bottom(self):
        """
        Check if any alien has reached the bottom of the screen.

        Returns:
            bool: True if any alien touches or passes the bottom edge.
        """
        alien: Alien
        for alien in self.fleet:
            if alien.rect.bottom >= self.settings.screen_h:
                return True
        return False
    
    def check_destroyed_status(self):
        """
        Determine if the entire fleet has been destroyed.

        Returns:
            bool: True if no aliens remain in the fleet.
        """
        return not self.fleet
