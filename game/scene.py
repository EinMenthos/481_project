import pygame, sys
from pygame.locals import *

# keeps track of game board size
ROWS = None
COLUMNS = None

# tracks the frame rate
FRAME_RATE = 30

class Scene:
    """Parent class for creating scenes."""
    def __init__(self, screen, background_color):
        """Initialize the scene and background"""
        self._screen = screen
        self._background = pygame.Surface(self._screen.get_size())
        self._background.fill(background_color)
        self._background.flip()
        self._frame_rate = FRAME_RATE

    def draw(self):
        """Draw the scene"""
        self._screen.blit(self._screen, (0, 0))

    def process_events(self, event):
        """Process a game event using the scene"""
        if event.type == pygame.QUIT:
            sys.exit(0)

class TitleScene(Scene):
    """Class used to create a Title Scene."""
    def __init__(self, screen, background_color):
        """Initialize the scene"""
        self._frame_rate = FRAME_RATE
        self._screen = screen
        self._background_color = background_color
        self._scene_is_running = True

    def start_scene(self):
        """Start the scene"""
        self._screen.fill(self._background_color)
    
    def draw(self):
        """Draw the scene"""
        super().draw()
    
    @property
    def scene_is_running(self):
        """Return True if the scene is running."""
        return self._scene_is_running
    
    def process_events(self, event):
        """Process game events using the scene"""
        super().process_events(event)