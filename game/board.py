import pygame
from .disk import Disk

class Board:
    """Creates an instance of Connect 4"""
    def __init__(self, screen, rows, cols):
        """Initialize the game board."""
        self._screen = screen
        self._rows = rows
        self._cols = cols
        self._rect = pygame.Rect(self.screen_width * 0.125, 150, self.screen_width * 0.75, self.screen_width * 0.75)
        self._disks = [Disk(self._screen, "red", (400, 400), 50)]
    @property
    def rect(self):
        """Returns the bounding rect"""
        return self._rect
    
    @property
    def screen_width(self):
        """Returns the screen's width"""
        return pygame.Surface.get_width(self._screen)
    
    @property
    def screen_height(self):
        """Returns the screen's height"""
        return pygame.Surface.get_height(self._screen)

    @property
    def disks(self):
        """Return list of disks"""
        return self._disks

    def draw(self):
        """Draws the game board and disks"""
        pygame.draw.rect(self._screen, (45,92,214), self.rect, border_radius=5)
        for disk in self.disks:
            disk.draw() 

    def process_events(self, event):
        """Process the game's events"""
