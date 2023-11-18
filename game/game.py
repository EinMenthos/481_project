import pygame
from pygame.locals import *
from game.scene import (
    TitleScene,
    VideoGameScene)

class Game:
    """Game class used to create an instance of Connect 4."""
    def __init__(
        self, height=800, width=800, window_title="Connect 4"
    ):
        """Iniitalize the game."""
        pygame.init()
        self._window_size = (width, height)
        self._clock = pygame.time.Clock()
        self._screen = pygame.display.set_mode(self._window_size)
        pygame.display.set_caption(window_title)
        self._scenes = []

    def create_scenes(self):
        """Create the scenes the game will use."""
        self._scenes = [TitleScene(self._screen, (30, 178, 247)),
            VideoGameScene(self._screen, (138,206,247))]
    
    def run(self):
        """Start and run each scene."""
        for scene in self._scenes:
            scene.start_scene()
            while scene.scene_is_running:
                scene.run()