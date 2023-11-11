import pygame, sys
from pygame.locals import *
from .button import Button

# keeps track of game board size
ROWS = None
COLUMNS = None

# tracks the frame rate
FRAME_RATE = 30

# tracks selection
SELECTION = None

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

    @property
    def screen_width(self):
        """Get the screen's width"""
        return pygame.Surface.get_width(self._screen) 

    @property
    def screen_height(self):
        """Get the screen's height"""
        return pygame.Surface.get_height(self._screen)
    
class TitleScene(Scene):
    """Class used to create a Title Scene."""
    def __init__(self, screen, background_color):
        """Initialize the scene"""
        self._frame_rate = FRAME_RATE
        self._screen = screen
        self._background_color = background_color
        self._scene_is_running = True
        self._buttons = [
            Button(self._screen, (int(self.screen_width * 0.875 - 50), self.screen_height * 0.33 + 75), "Play", 0, 100, 50, (0,0,255)),
            Button(self._screen, (int(self.screen_width * 0.875 - 50), self.screen_height * 0.50 + 75), "Play", 1, 100, 50, (0,0,255)),
            Button(self._screen, (int(self.screen_width * 0.875 - 25), self.screen_height * 0.80 + 75), "Settings", 2, 150, 50, (0,255,255))]
    def start_scene(self):
        """Start the scene"""
        self._screen.fill(self._background_color)
    
    def draw(self):
        """Draw the scene"""
        super().draw()

        # Draw "Connect 4" title
        title_rect = pygame.Rect(self.screen_width / 2 - 150, 50, 300, 100)
        font = pygame.font.Font(None, 100)
        text = font.render("Connect 4", True, (255, 255, 255))
        textpos = text.get_rect()
        textpos.centerx = title_rect.centerx
        textpos.centery = title_rect.centery
        self._screen.blit(text, textpos)
        self._screen.blit(text, textpos)

        # Draw "AI vs AI"
        option1_rect =  pygame.Rect(self.screen_width * 0.125, self.screen_height * 0.33, 600, 100)
        font = pygame.font.Font(None, 75)
        text = font.render("AI vs AI", True, (255, 255, 255))
        textpos = text.get_rect()
        textpos.centerx = option1_rect.centerx * 0.60 # shift left
        textpos.centery = option1_rect.centery
        self._screen.blit(text, textpos)
        self._screen.blit(text, textpos)

        # Draw "Player vs AI"
        option2_rect =  pygame.Rect(self.screen_width * 0.125 , self.screen_height * 0.50, 600, 100)
        font = pygame.font.Font(None, 75)
        text = font.render("Player vs AI", True, (255, 255, 255))
        textpos = text.get_rect()
        textpos.centerx = option2_rect.centerx * 0.7 # shift left
        textpos.centery = option2_rect.centery
        self._screen.blit(text, textpos)
        self._screen.blit(text, textpos)

        # draw buttons
        for button in self._buttons:
            button.draw()

    @property
    def scene_is_running(self):
        """Return True if the scene is running."""
        return self._scene_is_running
    
    def process_events(self, event):
        """Process game events using the scene"""
        super().process_events(event)
        for button in self._buttons:
            button.process_events(event)
            if button.clicked:
                self._scene_is_running = False

class VideoGameScene(Scene):
    """Class used to create an instance of Connect 4"""
    def __init__(self, screen, backgound_color):
        """Initialize the scene"""
        self._frame_rate = FRAME_RATE
        self._screen = screen
        self._background_color = backgound_color
        self._scene_is_running = True
    
    def start_scene(self):
        """Start the scene"""
        self._screen.fill(self._background_color)
    
    def draw(self):
        super().draw()

    @property
    def scene_is_running(self):
        """Return True if the scene is running."""
        return self._scene_is_running
    
    def process_events(self, event):
        """Process game events using the scene"""
        super().process_events(event)

    