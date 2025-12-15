"""
Button Module
Jonathan Carpenter

This module defines the HUD (Heads-Up Display) class, responsible for rendering
on-screen information such as the current score, max score in the session,
high score, level, and remaining ship lives in the Alien Invasion game.

date: 12/14/2025
"""

import pygame.font

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from alien_invasion import AlienInvasion

class Button:
    """
    A clickable button with centered text, used for UI elements like the Play button.

    Attributes:
        game (AlienInvasion): Reference to the main game instance.
        screen (pygame.Surface): The main game screen surface.
        boundaries (pygame.Rect): Rect representing the screen boundaries.
        settings (Settings): Game settings object containing colors, sizes, etc.
        font (pygame.font.Font): Font object used to render button text.
        rect (pygame.Rect): Rectangular area of the button.
        msg_image (pygame.Surface): Rendered image of the button's text.
        msg_image_rect (pygame.Rect): Rect for positioning the text image.
    """
    def __init__(self, game: 'AlienInvasion', msg):
        """
        Initialize the button and prepare its appearance.

        Args:
            game (AlienInvasion): The main game instance, providing access to screen,
                                  settings, and other game resources.
            msg (str): The text message to display on the button (e.g., "Play").

        Returns:
            None
        """
        self.game = game
        self.screen = game.screen
        self.boundaries = game.screen.get_rect()
        self.settings = game.settings
        self.font = pygame.font.Font(self.settings.font_file, self.settings.button_font_size)
        self.rect = pygame.Rect(0,0, self.settings.button_w, self.settings.button_h)
        self.rect.center = self.boundaries.center
        self._prep_msg(msg)

    def _prep_msg(self, msg):
        """
        Render the message text into an image and center it on the button.

        This private method converts the text string into a rendered image
        that can be blitted onto the screen.

        Args:
            msg (str): The text to render and display on the button.

        Returns:
            None
        """
        self.msg_image = self.font.render(msg, True, self.settings.text_color, None)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center
    
    def draw(self):
        """
        Draw the button on the screen.

        Fills the button rectangle with the background color and blits
        the text image on top.

        Args:
            None

        Returns:
            None
        """
        self.screen.fill(self.settings.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)

    def check_clicked(self, mouse_pos):
        """
        Determine if the button was clicked based on mouse position.

        Args:
            mouse_pos (tuple[int, int]): The current (x, y) position of the mouse cursor.

        Returns:
            bool: True if the mouse position is within the button's rectangle,
                  False otherwise.
        """
        return self.rect.collidepoint(mouse_pos)