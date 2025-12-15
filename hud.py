"""
HUD Module
Jonathan Carpenter

This module defines the HUD (Heads-Up Display) class, responsible for rendering
on-screen information such as the current score, max score in the session,
high score, level, and remaining ship lives in the Alien Invasion game.

date: 12/15/2025
"""

import pygame.font
# from alien_invasion import AlienInvasion
# from typing import TYPE_CHECKING

# if TYPE_CHECKING:
    


class HUD:
    """
    HUD class for showing game statistics and player lives.

    Displays the current score, session max score, all-time high score, current level,
    and remaining ship lives as small icons in the top portion of the screen.

    Attributes:
        game (AlienInvasion): Reference to the main game instance.
        settings (Settings): Game settings containing fonts, colors, and sizes.
        screen (pygame.Surface): The main game screen surface.
        boundaries (pygame.Rect): Rect representing the screen boundaries.
        game_stats (GameStats): Object holding current game statistics.
        font (pygame.font.Font): Font used for rendering text elements.
        padding (int): Space padding used for positioning elements.
    """
    def __init__(self, game):
        """
        Initialize the HUD and prepare all initial display elements.

        Args:
            game (AlienInvasion): The main game instance, providing access to screen,
                                  settings, stats, and other resources.

        Returns:
            None
        """
        self. game = game
        self.settings = game.settings
        self.screen = game.screen
        self.boundaries = game.screen.get_rect()
        self.game_stats = game.game_stats
        self.font = pygame.font.Font(self.settings.font_file, self.settings.HUD_font_size)
        self.padding = 20
        self._setup_life_image()
        self.update_scores()
        self.update_level()

    def _setup_life_image(self):
        """
        Load and scale the ship image used to represent remaining lives.

        Returns:
            None
        """
        self.life_image = pygame.image.load(self.settings.life_image)
        self.life_image = pygame.transform.scale(self.life_image, (self.settings.life_w, self.settings.life_h))
        self.life_rect = self.life_image.get_rect()


    def update_scores(self):
        """
        Update all score-related text elements (current score, session max score, high score).

        Should be called whenever any score value changes.

        Returns:
            None
        """
        self._update_max_score()
        self._update_score()
        self._update_hi_score()

    def _update_score(self):
        """
        Render the current score text and position it on the screen.

        Returns:
            None
        """
        score_str = f'Score: {self.game_stats.score: ,.0f}'
        self.score_image = self.font.render(score_str, True, self.settings.text_color, None)
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.boundaries.right - self.padding
        self.score_rect.top = self.max_score_rect.bottom + self.padding

    def _update_max_score(self):
        """
        Render the session max score text and position it on the screen.

        Returns:
            None
        """
        max_score_str = f'Max-Score: {self.game_stats.max_score: ,.0f}'
        self.max_score_image = self.font.render(max_score_str, True, self.settings.text_color, None)
        self.max_score_rect = self.max_score_image.get_rect()
        self.max_score_rect.right = self.boundaries.right - self.padding
        self.max_score_rect.top = self.padding

    def _update_hi_score(self):
        """
        Render the all-time high score text and position it centered at the top.

        Returns:
            None
        """
        hi_score_str = f'# High Score: {self.game_stats.hi_score: ,.0f} #'
        self.hi_score_image = self.font.render(hi_score_str, True, self.settings.text_color, None)
        self.hi_score_rect = self.hi_score_image.get_rect()
        self.hi_score_rect.right = self.boundaries.right - self.padding
        self.hi_score_rect.midtop = (self.boundaries.centerx, self.padding)

    def update_level(self):
        """
        Render the current level text and position it on the screen.

        Should be called whenever the level changes.

        Returns:
            None
        """
        level_str = f'Level: {self.game_stats.level: ,.0f}'
        self.level_image = self.font.render(level_str, True, self.settings.text_color, None)
        self.level_rect = self.level_image.get_rect()
        self.level_rect.left =  self.padding
        self.level_rect.top = self.life_rect.bottom + self.padding

    def _draw_lives(self):
        """
        Draw icons representing the player's remaining ships (lives) in the top-left corner.

        Draws one extra icon to represent the current active ship
        (total icons = ships_left + 1).

        Returns:
            None
        """
        current_x = self.padding
        current_y = self.padding
        for _ in range(self.game_stats.ships_left + 1):
            self.screen.blit(self.life_image, (current_x, current_y))
            current_x += self.life_rect.width + self.padding

    def draw(self):
        """
        Draw all HUD elements to the screen.

        This includes high score, max score, current score, level, and remaining lives.

        Returns:
            None
        """
        self.screen.blit(self.hi_score_image, self.hi_score_rect)
        self.screen.blit(self.max_score_image, self.max_score_rect)
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self._draw_lives()

