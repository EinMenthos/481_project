import pygame, sys
from pygame.locals import *
from .button import Button
from .board import Board
# keeps track of game board size
ROWS = None
COLUMNS = None

# tracks the frame rate
FRAME_RATE = 30

# tracks selection
SELECTION = None

TITLE_SCENE_INDEX = 0
SETTINGS_SCENE_INDEX = 1
VIDEOGAME_SCENE_INDEX = 2

class SceneManager:
    """Class to manage scenes in the game"""
    def __init__(self):
        self._scenes = []
        self._current_index = TITLE_SCENE_INDEX
        self._efs = []
    
    def add_scene(self, scene):
        """Adds a scene to be managed"""
        self._scenes.append(scene)

    def switch_scene(self, index):
        """Stops the current scene and starts runs a new scene"""
        # if the current scene is SettingsScene
        if self._current_index == SETTINGS_SCENE_INDEX:
            self._efs = self._scenes[self._current_index].items

        if 0 <= index < len(self._scenes):
            # stop the current scene
            self._scenes[self._current_index].scene_is_running = False
            self._scenes[self._current_index].requests_scene_switch = False
            self._scenes[self._current_index]._next_scene_index = None
            # update the new index
            self._current_index = index
            # start the new scene
            self._scenes[index].scene_is_running = True

            # if the new scene is VideoGameScene, set the evaluation functions
            if index == VIDEOGAME_SCENE_INDEX and len(self._efs) > 0:
                self._scenes[index].set_efs(self._efs)

    @property
    def current_scene(self):
        """Returns the current scene"""
        return self._scenes[self._current_index]

class Scene:
    """Parent class for creating scenes."""
    def __init__(self, screen, background_color):
        """Initialize the scene and background"""
        self._screen = screen
        self._background = pygame.Surface(self._screen.get_size())
        self._background.fill(background_color)
        self._background.flip()
        self._frame_rate = FRAME_RATE
        self._requests_scene_switch = False # tracks if new scene is going to run
        self._next_scene_index = None # tracks the index of new scene
        self._scene_is_running = True

    def draw(self):
        """Draw the scene"""
        self._screen.blit(self._screen, (0, 0))

    @property
    def screen_width(self):
        """Get the screen's width"""
        return pygame.Surface.get_width(self._screen) 

    @property
    def screen_height(self):
        """Get the screen's height"""
        return pygame.Surface.get_height(self._screen)
    
    @property
    def requests_scene_switch(self):
        """Returns True if current scene wants to switch scenes"""
        return self._requests_scene_switch
    
    @requests_scene_switch.setter
    def requests_scene_switch(self, value):
        """Updates the request for a scene switch"""
        self._requests_scene_switch = value

    @property
    def next_scene_index(self):
        """Returns the index of the next scene to run"""
        return self._next_scene_index
    
    @next_scene_index.setter
    def next_scene_index(self, value):
        """Updates the next scene index"""
        self._next_scene_index = value
    
    @property
    def scene_is_running(self):
        """Return True if the scene is running"""
        return self._scene_is_running

    @scene_is_running.setter
    def scene_is_running(self, status):
        """Set to True of False if the scene is running"""
        self._scene_is_running = status
    
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
            Button(self._screen, (int(self.screen_width * 0.875 - 25), self.screen_height * 0.80 + 75), "Settings", 2, 150, 50, (0,0,255))]
        self._requests_scene_switch = False # tracks if new scene is going to run
        self._next_scene_index = None # tracks the index of new scene

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
    
    def run(self):
        """Process game events for the scene"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            for button in self._buttons:
                button.process_events(event)
                if button.clicked:
                    # stop the current scene
                    self._scene_is_running = False

                    # unclick the button
                    button.toggle()

                    # update the selection choice
                    global SELECTION
                    SELECTION = button.value

                    # make a request to switch scenes
                    self._requests_scene_switch = True 

                    # set the new scene index
                    if SELECTION == 0 or SELECTION == 1:
                        self._next_scene_index = VIDEOGAME_SCENE_INDEX # VideoGameScene is the next scene
                    elif SELECTION == 2:
                        self._next_scene_index = SETTINGS_SCENE_INDEX # SettingsScene is the next scene
            self.draw()
            pygame.display.update()

class VideoGameScene(Scene):
    """Class used to create an instance of Connect 4"""
    def __init__(self, screen, backgound_color):
        """Initialize the scene"""
        self._frame_rate = FRAME_RATE
        self._screen = screen
        self._background_color = backgound_color
        self._scene_is_running = True
        self._board = None
        self._requests_scene_switch = False # tracks if new scene is going to run
        self._next_scene_index = None   # tracks the index of new scene
        self._efs = [
            {"name": "EV1: conquer the center", "selected": False},
            {"name": "EV2: 7 trap", "selected": False},
            {"name": "EV3: Surrounding discs", "selected": False},
            {"name": "EV4: Block 7 traps", "selected": False},
            {"name": "EV5: fork 10", "selected": False},
            {"name": "EV6: fork 25", "selected": False}
        ]

    def set_efs(self, efs):
        """Sets the evaluation functions to be used"""
        self._efs = efs

    def start_scene(self):
        """Start the scene"""
        self._board = Board(self._screen, 6, 7, SELECTION, self._efs)
        self._screen.fill(self._background_color)
    
    def draw(self):
        super().draw()
        # draw the game board and pieces
        self._board.draw()

    def run(self):
        """Runs an instance of Connect 4"""
        self._board.run()

class SettingsScene(Scene):
    """Class used to create a Settings Scene."""
    def __init__(self, screen, background_color):
        """Initialize the scene"""
        self._frame_rate = FRAME_RATE
        self._screen = screen
        self._background_color = background_color
        self._scene_is_running = True
        self._items = [
            {"name": "EV1: conquer the center", "selected": False},
            {"name": "EV2: 7 trap", "selected": False},
            {"name": "EV3: Surrounding discs", "selected": False},
            {"name": "EV4: Block 7 traps", "selected": False},
            {"name": "EV5: fork 10", "selected": False},
            {"name": "EV6: fork 25", "selected": False}
        ]
        self._buttons = [
            Button(self._screen, (150, int(self.screen_width * 0.125)), "Back", 0, 100, 50, (0, 0, 255))
        ]
        self._requests_scene_switch = False # tracks if new scene is going to run
        self._next_scene_index = None   # tracks the index of new scene

    @property
    def items(self):
        """Return the selected evaluation functions"""
        return self._items

    def start_scene(self):
        """Start the scene"""
        self._screen.fill(self._background_color)

    def draw(self):
        """Draw the scene"""
        super().draw()

        # Draw title
        title_rect = pygame.Rect(self.screen_width / 2 - 150, 50, 300, 100)
        font = pygame.font.Font(None, 100)
        text = font.render("Settings AI 2", True, (255, 255, 255))
        textpos = text.get_rect()
        textpos.centerx = title_rect.centerx
        textpos.centery = title_rect.centery
        self._screen.blit(text, textpos)

        # Draw items
        item_height = 200
        font = pygame.font.Font(None, 50)
        checkbox_width = 20
        checkbox_margin = 10

        for item in self._items:
            # Draw checkbox
            checkbox_rect = pygame.Rect(self.screen_width / 2 - 200, item_height - 25, checkbox_width, checkbox_width)
            pygame.draw.rect(self._screen, (255, 255, 255), checkbox_rect, 2)
            if item["selected"]:
                pygame.draw.line(self._screen, (255, 255, 255), (checkbox_rect.left + 5, checkbox_rect.centery),
                                (checkbox_rect.centerx, checkbox_rect.bottom - 5), 2)
                pygame.draw.line(self._screen, (255, 255, 255), (checkbox_rect.centerx, checkbox_rect.bottom - 5),
                                (checkbox_rect.right - 5, checkbox_rect.top + 5), 2)

            # Draw text
            text = font.render(item["name"], True, (255, 255, 255))
            textpos = text.get_rect()
            textpos.left = checkbox_rect.right + checkbox_margin  # Adjust the horizontal position
            textpos.centery = item_height - 15
            self._screen.blit(text, textpos)

            item_height += 50

        # Draw buttons
        for button in self._buttons:
            button.draw()

        pygame.display.update()

    def toggle_item(self, index):
        """Toggle the selected state of an item."""
        self._items[index]["selected"] = not self._items[index]["selected"]

    def run(self):
        """Process game events for the scene"""
        while self._scene_is_running:
            button_clicked = False  # Flag to track whether a button was clicked

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)

                # Handle checkbox clicks
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    for i, item in enumerate(self._items):
                        checkbox_rect = pygame.Rect(self.screen_width / 2 - 200, 200 + 50 * i - 25, 20, 20)
                        if checkbox_rect.collidepoint(event.pos):
                            self.toggle_item(i)
                            print(f"{item['name']} {'selected' if item['selected'] else 'deselected'}")

                for button in self._buttons:
                    button.process_events(event)
                    if button.clicked:
                        button_clicked = True  # Set the flag to True when a button is clicked

            if button_clicked and event.type == pygame.MOUSEBUTTONUP:
                # Process the button click only once when the mouse button is released
                for button in self._buttons:
                    if button.clicked:
                        # stop the current scene
                        button.toggle()
                        # request and update new scene index
                        self._scene_is_running = False
                        self._requests_scene_switch = True
                        self._next_scene_index = TITLE_SCENE_INDEX # next scene is TitleScene

            # Clear the screen
            self._screen.fill(self._background_color)

            self.draw()
            pygame.display.update()