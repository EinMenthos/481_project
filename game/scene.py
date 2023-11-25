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
            Button(self._screen, (int(self.screen_width * 0.875 - 25), self.screen_height * 0.80 + 75), "Settings", 2, 150, 50, (0,0,255))]
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
    
    def run(self):
        """Process game events for the scene"""
        while self._scene_is_running:
            button_clicked = False  # Flag to track whether a button was clicked

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit(0)
                for button in self._buttons:
                    button.process_events(event)
                    if button.clicked:
                        button_clicked = True  # Set the flag to True when a button is clicked

                if button_clicked and event.type == pygame.MOUSEBUTTONUP:
                    # Process the button click only once when the mouse button is released
                    for button in self._buttons:
                        if button.clicked:
                            if button.value == 2:  # Check if the "Settings" button is clicked
                                # Create and run the SettingsScene
                                settings_scene = SettingsScene(self._screen, (30, 178, 247))
                                settings_scene.start_scene()
                                while settings_scene.scene_is_running:
                                    settings_scene.run()
                                    #print("loop")
                                # Return to the main loop after exiting the SettingsScene
                                self.start_scene()  # Reset the TitleScene
                            else:
                                # stop the current scene
                                self._scene_is_running = False
                                # update the selection choice
                                global SELECTION
                                SELECTION = button.value

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
    
    def start_scene(self):
        """Start the scene"""
        self._board = Board(self._screen, 6, 7, SELECTION)
        self._screen.fill(self._background_color)
    
    def draw(self):
        super().draw()
        # draw the game board and pieces
        self._board.draw()

    @property
    def scene_is_running(self):
        """Return True if the scene is running."""
        return self._scene_is_running
    
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
            {"name": "EV5: 7 trap2", "selected": False},
            {"name": "EV6: Horizontal trap", "selected": False}
        ]
        self._buttons = [
            Button(self._screen, (int(self.screen_width * 0.5 - 50), 100), "Back", 0, 100, 50, (0, 0, 255))
        ]

    def start_scene(self):
        """Start the scene"""
        self._screen.fill(self._background_color)

    def draw(self):
        """Draw the scene"""
        super().draw()

        # Draw title
        title_rect = pygame.Rect(self.screen_width / 2 - 150, 50, 300, 100)
        font = pygame.font.Font(None, 100)
        text = font.render("Settings AI2", True, (255, 255, 255))
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
            checkbox_rect = pygame.Rect(self.screen_width / 2 - 100, item_height - 25, checkbox_width, checkbox_width)
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
        #self.draw()  # Redraw the screen to update the checkbox visually

    @property
    def scene_is_running(self):
        """Return True if the scene is running."""
        return self._scene_is_running

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
                        checkbox_rect = pygame.Rect(self.screen_width / 2 - 100, 200 + 50 * i - 25, 20, 20)
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
                        if button.value == 0:  # Check if the "Back" button is clicked
                            # stop the current scene
                            self._scene_is_running = False
                        else:
                            # Handle other buttons if needed
                            pass

            # Clear the screen
            self._screen.fill(self._background_color)

            self.draw()
            pygame.display.update()
