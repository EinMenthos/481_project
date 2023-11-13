import pygame, random
from .disk import Disk
from .player import Player

class Board:
    """Creates an instance of Connect 4"""
    def __init__(self, screen, rows, cols, game_type):
        """Initialize the game board."""
        self._screen = screen
        self._rows = rows
        self._cols = cols
        self._game_type = game_type
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
        self._players = [] # list of players
        self.initialize_players() # create the players
        self._continue_playing = True

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

    def initialize_players(self):
        """Creates the players for the game and selects order"""
        colors = ["red", "yellow"] # disk colors

        random.shuffle(colors) # shuffle the colors

        # create a list of 2 players
        if self._game_type == 0: # AI vs AI
            self._players = [Player(colors[0], False), Player(colors[1], False)]
        else: # AI vs Human
            self._players = [Player(colors[0], False), Player(colors[1], True)]

        # shuffle the list of players 
        random.shuffle(self._players)    

    def draw(self):
        """Draws the game board and disks"""
        pygame.draw.rect(self._screen, (45,92,214), self.rect, border_radius=5)
        for i, row in enumerate(self.disks):
            for j, disk in enumerate(row):
                disk.draw() 

    def process_events(self, event):
        """Process the game's events"""
        # run until player quits
        while self._continue_playing:
            # tracks the current player
            player_index = 0

            # runs an instance (game) of Connect 4 based on a circular queue
            while True:
                current_player = self._players[player_index]

                # check if player is human
                if current_player.is_human:
                    pass
                else:
                    pass
                # switch players in order
                player_index = (player_index + 1) % 2




