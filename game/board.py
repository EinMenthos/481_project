import pygame, random, sys, time
from .disk import Disk
from .player import Player

class Board:
    """Creates an instance of Connect 4"""
    def __init__(self, screen, rows, cols, game_type, connect=4):
        """Initialize the game board."""
        self._screen = screen
        self._rows = rows
        self._cols = cols
        self._game_type = game_type # 0 = AI vs AI, 1 = AI vs Player
        self._connect = connect # how many disks to connect in a row to win
        self._rect = pygame.Rect(int(self.screen_width * 0.125), int(self.screen_height * 0.25), int(self.screen_width * 0.75), int(self.screen_height * 0.75))
        self._disk_width = int((self._rect.width / cols) * 0.75) # width of 1 disk
        self._disk_height = int((self._rect.height / rows) * 0.75) # height of 1 disk
        self._disk_diameter = min(self._disk_width, self._disk_height) # pick the smallest between width and height to set as diameter
        self._disk_radius =  self._disk_diameter / 2 # set the radius
        self._gap_x = (self._rect.width - (self._disk_diameter * cols)) // (cols + 1) # set the gap between columns
        self._gap_y = (self._rect.height - (self._disk_diameter * rows)) // (rows + 1) # set the gap between rows
        # create the disks
        self._disks = self.init_disks()
        self._col_pos = [disk.center[0] for disk in self._disks[0]] # column center points
        self._col_rects = [
            pygame.Rect(x - self._disk_radius, self._rect.top, self._disk_diameter, self.rect.height) 
            for x in self._col_pos
        ]
        self._players = [] # list of players
        self.initialize_players() # create the players
        self._preview_disk = Disk(self._screen, "red", (self._col_pos[0],150), self._disk_diameter) # disk on top of board 
        self._continue_playing = True
        self._player_index = 0 # tracks the current player
        self._font = pygame.font.Font(None, 60) # font for Player's Turn Text
        self._new_game = False

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
    
    def init_disks(self):
        """Initialize the disks for a new instance of Connect 4"""
        return [
            [Disk(
                self._screen,
                "white", 
                (
                    self._rect.left + ((j + 1) * self._gap_x) + (self._disk_diameter * j) + self._disk_radius,
                    self._rect.top + ((i + 1) * self._gap_y) + (self._disk_diameter * i) + self._disk_radius
                ),
                self._disk_diameter
            ) 
            for j in range(self._cols)] for i in range(self._rows)
        ]

    def initialize_players(self):
        """Creates the players for the game and selects order"""
        colors = ["red", "yellow"] # disk colors

        random.shuffle(colors) # shuffle the colors

        # create a list of 2 players
        if self._game_type == 0: # AI vs AI
            self._players = [Player(colors[0], False), Player(colors[1], False)]
        else: # AI vs Human
            self._players = [Player(colors[0], True), Player(colors[1], True)]

        # shuffle the list of players 
        random.shuffle(self._players)    

    def draw(self):
        """Draws the game board and disks"""
        # clear the screen
        self._screen.fill((138,206,247))

        # draw the game board
        pygame.draw.rect(self._screen, (45,92,214), self.rect, border_radius=5)

        # draw each disk
        for i, row in enumerate(self.disks):
            for j, disk in enumerate(row):
                disk.draw() 
        
        # draw the preview disk on top
        self._preview_disk.draw()

        # create text to show current player
        text = self._font.render(f"Player {self._player_index + 1}'s Turn", True, (255, 255, 255))
        textpos = text.get_rect()
        textpos.left = self._rect.left
        textpos.centery = int(self.screen_height * 0.10)

        # draw the text
        self._screen.blit(text, textpos)

    def make_move(self, col, color):
        """Player makes a move. Returns True if move made successfully."""
        # iterate through all of the rows in a column 
        for row in range(len(self._disks) - 1, -1, -1):
            # if the row is white (empty), then change the color
            if self._disks[row][col].is_empty():
                # change color to represent dropping a disk
                self._disks[row][col].color = color
                return True
            
        # move cannot be made, return False
        return False

    def check_winner(self, player):
        """Returns True if the current player is a winner"""
        for row in range(self._rows):
            for col in range(self._cols):
                if self._disks[row][col].color == player:
                    # Check horizontally
                    if col + self._connect <= self._cols and all(self._disks[row][col+i].color == player for i in range(self._connect)):
                        return True
                    # Check vertically
                    if row + self._connect <= self._rows and all(self._disks[row+i][col].color == player for i in range(self._connect)):
                        return True
                    # Check diagonally (positive slope)
                    if col + self._connect <= self._cols and row + self._connect <= self._rows and all(self._disks[row+i][col+i].color == player for i in range(self._connect)):
                        return True
                    # Check diagonally (negative slope)
                    if col - self._connect + 1 >= 0 and row + self._connect <= self._rows and all(self._disks[row+i][col-i].color == player for i in range(self._connect)):
                        return True
        return False
    
    def run(self):
        """Process the game's events"""
        # run until player quits
        while self._continue_playing:
            # if starting a 2nd game... 
            if self._new_game:
                # change the new game flag to False
                self._new_game = False

                # clear the disks
                self._disks = self.init_disks()

                # loser who lost the previous game starts first, change later

            # tracks if player made a move
            move_made = False

            # runs an instance (game) of Connect 4 based on a circular queue
            while not move_made:
                current_player = self._players[self._player_index]
                
                # update the preview disk's color to current player's color
                self._preview_disk.color = current_player.color

                # handle events
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit(0)
                    
                    # check if player is human
                    if current_player.is_human:
                        # get the mouse's current position
                        point = pygame.mouse.get_pos()                                     
                        
                        # check if cursor is touching a column
                        for col, rect in enumerate(self._col_rects):
                            if event.type == pygame.MOUSEMOTION:
                                # if cursor is on a column, change the preview
                                #  disk's center to the column's center
                                if rect.collidepoint(point[0], point[1]):
                                    self._preview_disk.center = (rect.center[0], 150)
                                    break

                            # if clicking on a column, attempt to drop a disk
                            if rect.collidepoint(point) and event.type == pygame.MOUSEBUTTONDOWN:
                                if self.make_move(col, current_player.color):
                                    # move was made, change flag to true to stop current player's turn
                                    move_made = True

                                    # check if player is a winner
                                    if self.check_winner(current_player.color):
                                        print("play again?")
                                        self._new_game = True
                                    break
                    else:
                        pass

                    self.draw()

                    pygame.display.update()

            # switch players in order
            self._player_index = (self._player_index + 1) % 2