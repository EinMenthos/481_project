import pygame
from .disk import Disk

class Board:
    """Creates an instance of Connect 4"""
    def __init__(self, screen, rows, cols):
        """Initialize the game board."""
        self._screen = screen
        self._rows = rows
        self._cols = cols
        self._rect = pygame.Rect(int(self.screen_width * 0.125), int(self.screen_height * 0.25), int(self.screen_width * 0.75), int(self.screen_height * 0.75))
        self._disk_width = int((self._rect.width / cols) * 0.75) # width of 1 disk
        self._disk_height = int((self._rect.height / rows) * 0.75) # height of 1 disk
        self._disk_diameter = min(self._disk_width, self._disk_height) # pick the smallest between width and height to set as diameter
        self._disk_radius =  self._disk_diameter / 2 # set the radius
        self._gap_x = (self._rect.width - (self._disk_diameter * cols)) // (cols + 1) # set the gap between columns
        self._gap_y = (self._rect.height - (self._disk_diameter * rows)) // (rows + 1) # set the gap between rows
        # create the disks
        self._disks = [
            [Disk(
                screen,
                "white", 
                (
                    self._rect.left + ((j + 1) * self._gap_x) + (self._disk_diameter * j) + self._disk_radius,
                    self._rect.top + ((i + 1) * self._gap_y) + (self._disk_diameter * i) + self._disk_radius
                ),
                self._disk_width
            ) 
            for j in range(self._cols)] for i in range(self._rows)]
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
        for i, row in enumerate(self.disks):
            for j, disk in enumerate(row):
                disk.draw() 
    def process_events(self, event):
        """Process the game's events"""
