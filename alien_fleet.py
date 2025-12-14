import pygame
from alien import Alien
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class AlienFleet:

    def __init__(self, game: 'AlienInvasion'):
        self.game = game
        self.settings = game.settings
        self.fleet = pygame.sprite.Group()
        self.fleet_direction = self.settings.fleet_direction
        self.fleet_drop_speed = self.settings.fleet_drop_speed

        self.create_fleet()

    def create_fleet(self):
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
        for row in range(fleet_h):
            for col in range(fleet_w):
                # Place alien on main diagonal or anti-diagonal
                if col == row or col == (fleet_w - 1 - row):
                    current_x = col * alien_w + x_offset
                    current_y = row * alien_h + y_offset
                    self._create_alien(current_x, current_y)

    def _create_rectangle_fleet(self, alien_w, alien_h, fleet_w, fleet_h, x_offset, y_offset):
        for row in range(fleet_h):
            for col in range (fleet_w):
                current_x = alien_w * col + x_offset
                current_y = alien_h * row + y_offset
                if col % 2 == 0 or row % 2 == 0:
                    continue
                self._create_alien(current_x, current_y)

    def calculate_fleet_size(self, alien_w, screen_w, alien_h, screen_h):
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
        new_alien = Alien(self, current_x, current_y)
        self.fleet.add(new_alien)

    def _check_fleet_edges(self):
        alien: Alien
        for alien in self.fleet:
            if alien.check_edges():
                self._drop_alien_fleet()
                self.fleet_direction *= -1
                break

    def _drop_alien_fleet(self):
        for alien in self.fleet:
            alien.y += self.fleet_drop_speed

    def update_fleet(self):
        self._check_fleet_edges()
        self.fleet.update()

    def draw(self):
        alien: 'Alien'
        for alien in self.fleet:
            alien.draw_alien()

    def check_collisions(self, other_group):
        return pygame.sprite.groupcollide(self.fleet, other_group, True, True)

    def check_fleet_bottom(self):
        alien: Alien
        for alien in self.fleet:
            if alien.rect.bottom >= self.settings.screen_h:
                return True
        return False
    
    def check_destroyed_status(self):
        return not self.fleet
