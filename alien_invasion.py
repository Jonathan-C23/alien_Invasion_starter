"""
Star Wars Alien Invasion
Jonathan Carpenter

This is the main module for the Alien Invasion game with a Star Wars theme.
It initializes pygame, sets up the game window, loads assets, manages the main
game loop, handles events, updates game objects, checks collisions, and
coordinates all game components.

date: 12/14/2025
"""

import sys
import pygame
from settings import Settings
from game_stats import GameStats
from ship import Ship
from arsenal import Arsenal
# from alien import Alien
from alien_fleet import AlienFleet
from time import sleep
from button import Button
from hud import HUD


class AlienInvasion:
    """
    Main game class that manages assets, behavior, and the overall flow of the game.

    Coordinates all game elements including the ship, alien fleet, arsenal (bullets),
    HUD, play button, sounds, and game statistics.

    Attributes:
        settings (Settings): Game configuration and dynamic settings.
        screen (pygame.Surface): The main display surface.
        bg (pygame.Surface): Scaled background image.
        clock (pygame.time.Clock): Controls frame rate.
        game_stats (GameStats): Tracks scores, lives, level, and persistent high score.
        HUD (HUD): Heads-up display for showing scores and lives.
        ship (Ship): Player-controlled ship instance.
        alien_fleet (AlienFleet): Manages the fleet of aliens.
        play_button (Button): Play button shown when the game is inactive.
        game_active (bool): Flag indicating whether the game is currently running.
        running (bool): Flag controlling the main game loop.
        Various pygame.mixer.Sound objects for laser, impact, and background music.
    """

    def __init__(self):
        """
        Initialize the game, create resources, and set up initial game objects.

        Returns:
            None
        """
        pygame.init()
        self.settings = Settings()
        self.settings.initialize_dynamic_settings()

        self.screen = pygame.display.set_mode((self.settings.screen_w,self.settings.screen_h))
        pygame.display.set_caption(self.settings.name)

        self.bg = pygame.image.load(self.settings.bg_file)
        self.bg = pygame.transform.scale(self.bg, (self.settings.screen_w, self.settings.screen_h))

        self.game_stats = GameStats(self)
        self.HUD = HUD(self)
        self.running = True
        self.clock = pygame.time.Clock()

        pygame.mixer.init()
        self.laser_sound = pygame.mixer.Sound(self.settings.laser_sound)
        self.laser_sound.set_volume(0.7)
        self.impact_sound = pygame.mixer.Sound(self.settings.impact_sound)
        self.impact_sound.set_volume(0.2)
        self.music = pygame.mixer.Sound(self.settings.music)
        self.music.set_volume(0.4)
        self.music.play(-1)

        self.ship = Ship(self, Arsenal(self))
        self.alien_fleet = AlienFleet(self)
        self.alien_fleet.create_fleet()


        self.play_button = Button(self, 'Play')
        self.game_active = False

    def run_game(self):
        """
        Start the main game loop.

        Handles events, updates game state when active, and redraws the screen.

        Returns:
            None
        """
        # Game loop
        while self.running:
            self._check_events()
            if self.game_active:
                self.ship.update()
                self.alien_fleet.update_fleet()
                self._check_collisions()
            self._update_screen()
            self.clock.tick(self.settings.FPS)
    
    def _check_collisions(self):
        """
        Check for and handle all major collisions in the game.

        Handles ship-alien collisions, bullet-alien collisions, and level completion.

        Returns:
            None
        """
        if self.ship.check_collisions(self.alien_fleet.fleet):
            self._check_game_stats()
        collisions = self.alien_fleet.check_collisions(self.ship.arsenal.arsenal)
        if collisions:
            self.impact_sound.play()
            self.impact_sound.fadeout(800)
            self.game_stats.update(collisions)
            self.HUD.update_scores()
        
        if self.alien_fleet.check_destroyed_status():
            self._reset_level()
            self.settings.increase_difficulty()
            self.HUD.update_scores()
            self.game_stats.update_level()
            self.HUD.update_level()
    
    def _check_game_stats(self):
        """
        Handle the consequences of the ship being hit by an alien.

        Decrements lives, resets the level if lives remain, or ends the game.

        Returns:
            None
        """
        if self.game_stats.ships_left > 0:
            self.game_stats.ships_left -= 1
            self._reset_level()
            sleep(0.5)
        else:
            self.game_active = False
            


    def _reset_level(self):
        """
        Clear bullets and aliens, then recreate the alien fleet for a new level or retry.

        Returns:
            None
        """
        self.ship.arsenal.arsenal.empty()
        self.alien_fleet.fleet.empty()
        self.alien_fleet.create_fleet()

    def _restart_game(self):
        """
        Restart the game from a fresh state when the Play button is clicked.

        Resets dynamic settings, stats, centers the ship, hides the mouse, and starts music.

        Returns:
            None
        """
        self.settings.initialize_dynamic_settings()
        self.game_stats.reset_stats()
        self.HUD.update_scores()
        self._reset_level()
        self.ship._center_ship()
        self.game_active = True
        pygame.mouse.set_visible(False)

        self.music.stop()
        self.music.play(-1)

    def _update_screen(self):
        """
        Update and redraw all game elements on the screen.

        Draws background, ship, aliens, HUD, and the play button when inactive.

        Returns:
            None
        """
        self.screen.blit(self.bg, (0,0))
        self.ship.draw()
        self.alien_fleet.draw()
        self.HUD.draw()


        if not self.game_active:
            self.play_button.draw()
            pygame.mouse.set_visible(True)

        pygame.display.flip()

    def _check_events(self):
        """
        Respond to keyboard, mouse, and window events.

        Returns:
            None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.game_stats.save_scores()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and self.game_active == True:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._check_button_clicked()
    
    def _check_button_clicked(self):
        """
        Check if the Play button was clicked and restart the game if so.

        Returns:
            None
        """
        mouse_pos = pygame.mouse.get_pos()
        if self.play_button.check_clicked(mouse_pos):
            self._restart_game()
    
    def _check_keyup_events(self, event):
        """
        Handle key release events (stop ship movement).

        Args:
            event (pygame.event.Event): The keyup event.

        Returns:
            None
        """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self. ship.moving_left = False
        
    def _check_keydown_events(self, event):
        """
        Handle key press events (movement, firing, quit).

        Args:
            event (pygame.event.Event): The keydown event.

        Returns:
            None
        """
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE:
            if self.ship.fire():
                # play the laser sound
                self.laser_sound.play()
                self.laser_sound.fadeout(500)

        elif event.key == pygame.K_q:
            self.running = False
            self.game_stats.save_scores()
            pygame.quit()
            sys.exit()

if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
