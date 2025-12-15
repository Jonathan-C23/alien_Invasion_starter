"""
GameStats Module
Jonathan Carpenter

This module defines the GameStats class, which tracks and manages dynamic
statistics for the Alien Invasion game, including score, level, lives remaining,
session max score, and persistent high score saved to a JSON file.

date: 12/14/2025
"""

import json
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class GameStats():
    """
    Tracks statistics for the Alien Invasion game.

    Manages both runtime statistics (score, level, ships left, session max score)
    and persistent data (all-time high score saved to a file).

    Attributes:
        game (AlienInvasion): Reference to the main game instance.
        settings (Settings): Game settings containing initial values and file paths.
        score (int): Current score in the active game.
        max_score (int): Highest score achieved in the current session.
        hi_score (int): All-time high score loaded from/saved to file.
        level (int): Current game level.
        ships_left (int): Number of remaining ships (lives).
        path (pathlib.Path): Path to the JSON file storing the high score.
    """
    def __init__(self, game: 'AlienInvasion'):
        """
        Initialize game statistics and load persistent high score if available.

        Args:
            game (AlienInvasion): The main game instance, providing access to settings.

        Returns:
            None
        """
        self.game = game
        self.settings = game.settings
        self.max_score = 0
        self.score = 0
        self.level = 1
        self.init_saved_scores()
        self.reset_stats()

    def init_saved_scores(self):
        """
        Load the all-time high score from a JSON file if it exists and is valid.

        If the file is missing, empty, or too small, initializes high score to 0
        and creates a new file.

        Returns:
            None
        """
        self.path = self.settings.scores_file
        if self.path.exists() and self.path.stat.__sizeof__() > 40:
            contents = self.path.read_text()
            scores = json.loads(contents)
            self.hi_score = scores.get('hi_score', 0)
        else:
            self.hi_score = 0
            self.save_scores()
    
    def save_scores(self):
        """
        Save the current all-time high score to a JSON file.

        Attempts to write the high score to the file. Prints an error if the file
        cannot be found or written.

        Returns:
            None
        """
        scores = {
            'hi_score': self.hi_score
        }
        contents = json.dumps(scores, indent=4)
        try:
            self.path.write_text(contents)
        except FileNotFoundError as e:
            print(f'File Not Found: {e}')

    def reset_stats(self):
        """
        Reset statistics that change during a new game.

        Called when starting a new game to reset lives, score, and level
        while preserving max_score and hi_score.

        Returns:
            None
        """
        self.ships_left = self.settings.starting_ship_count
        self.score = 0
        self.level = 1

    def update(self, collisions):
        """
        Update score-related statistics based on recent alien collisions.

        Args:
            collisions (dict): Dictionary of collided sprites (typically aliens).

        Returns:
            None
        """
        self._update_score(collisions)
        self._update_max_score()
        self._update_high_score()

    def _update_max_score(self):
        """
        Update the session max score if the current score is higher.

        Returns:
            None
        """
        if self.score > self.max_score:
            self.max_score = self.score

    def _update_high_score(self):
        """
        Update the all-time high score if the current score is higher.

        Returns:
            None
        """
        if self.score > self.hi_score:
            self.hi_score = self.score

    def _update_score(self, collisions):
        """
        Add points to the current score based on destroyed aliens.

        Args:
            collisions (dict): Dictionary containing collided alien sprites.

        Returns:
            None
        """
        for alien in collisions.values():
            self.score += self.settings.alien_points

    def update_level(self):
        """
        Increment the game level.

        Typically called when the player clears all aliens on the screen.

        Returns:
            None
        """
        self.level += 1