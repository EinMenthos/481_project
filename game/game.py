import pygame
from pygame.locals import *
from game.scene import (
    TitleScene,
    VideoGameScene,
    SettingsScene, 
    SceneManager)

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
        self._scene_manager = SceneManager() # create scene manager

    def run(self):
        """Start and run each scene."""
        # create the new scenes for the manager to run
        self._scene_manager.add_scene(TitleScene(self._screen, (30, 178, 247)))
        self._scene_manager.add_scene(SettingsScene(self._screen, (138,206,247)))
        self._scene_manager.add_scene(VideoGameScene(self._screen, (138,206,247)))

        while True:
            # get the current scene
            scene = self._scene_manager.current_scene
            # start the current scene
            scene.start_scene()
            # run the scene
            scene.run()

            # switch scenes if requested
            if scene.requests_scene_switch:
                self._scene_manager.switch_scene(scene._next_scene_index)