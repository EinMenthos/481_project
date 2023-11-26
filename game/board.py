import pygame, random, sys, time, copy
from .disk import Disk
from .player import Player
from .popup import Popup
from .button import Button

class Board:
    """Creates an instance of Connect 4"""
    def __init__(self, screen, rows, cols, game_type, efs, connect=4):
        """Initialize the game board."""
        self._screen = screen
        self._rows = rows
        self._cols = cols
        self._game_type = game_type # 0 = AI vs AI, 1 = AI vs Player
        self._efs = efs
        self._connect = connect # how many disks to connect in a row to win
        self._frame_rate = 10
        self._clock = pygame.time.Clock()
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
        self._preview_disk = Disk(self._screen, "red", (self._col_pos[0],150), self._disk_diameter) # disk on top of board 
        self._continue_playing = True
        self._player_index = 0 # tracks the current player
        self._opponent_index = 1 # tracks the opponent's index 
        self._font = pygame.font.Font(None, 60) # font for Player's Turn Text
        self._new_game = False
        self._game_over = False
        self._game_over_popup = Popup(screen, (self._rect.left, self._rect.top), [
            Button(screen, (325, 600), "Quit", False, 150, 50, (0,0,255)),
            Button(screen, (600, 600), "Play Again", True, 150, 50, (0,0,255))
        ],
        (self._rect.width, self._rect.height))

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
            self._players = [Player(colors[0], False, ef_mode=False), 
                Player(
                    colors[1], 
                    False, ef_mode=True, 
                    ev1_set=self._efs[0]["selected"], 
                    ev2_set=self._efs[1]["selected"],
                    ev3_set=self._efs[2]["selected"],
                    ev4_set=self._efs[3]["selected"],
                    ev5_set=self._efs[4]["selected"],
                    ev6_set=self._efs[5]["selected"],
                )]
            
        else: # AI vs Human
            self._players = [Player(colors[0], False, ef_mode=False), Player(colors[1], True)]

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

        # if the game is over, draw the popup
        if self._game_over:
            self._game_over_popup.draw()

    def make_move(self, board, col, player):
        """Player makes a move. Update the board."""
        # iterate through all of the rows in a column 
        for row in range(len(board) - 1, -1, -1):
            # if the row is white (empty), then change the color
            if board[row][col].is_empty():
                # change color to represent dropping a disk
                board[row][col].color = player.color
                break

    def check_winner(self, board, player):
        """Returns True if the current player is a winner"""
        for row in range(self._rows):
            for col in range(self._cols):
                if board[row][col].color == player.color:
                    # Check horizontally
                    if col + self._connect <= self._cols and all(board[row][col+i].color == player.color for i in range(self._connect)):
                        return True
                    # Check vertically
                    if row + self._connect <= self._rows and all(board[row+i][col].color == player.color for i in range(self._connect)):
                        return True
                    # Check diagonally (positive slope)
                    if col + self._connect <= self._cols and row + self._connect <= self._rows and all(board[row+i][col+i].color == player.color for i in range(self._connect)):
                        return True
                    # Check diagonally (negative slope)
                    if col - self._connect + 1 >= 0 and row + self._connect <= self._rows and all(board[row+i][col-i].color == player.color for i in range(self._connect)):
                        return True
        return False
    
    def is_full(self, board):
        """Returns true if board is full (no more available moves)"""
        return all(cell.is_empty() != True for cell in board[0])
    
    def is_valid_move(self, board, col):
        """Returns True if a valid move (player can drop a disk in that column)"""
        return board[0][col].is_empty()
    
    def evaluate_window(self, window, player, EFmode):
        print(f"{self._player_index}: efmode={EFmode}, ef1={player.ev1_set}, ef2={player.ev2_set}, ef3={player.ev3_set}, ef4={player.ev4_set}, ef5={player.ev5_set}, ef6={player.ev6_set}")
        score = 0

        opponent = self._players[self._opponent_index] 

        if window.count(player.color) == 4:
            score += 100
        elif window.count(player.color) == 3 and window.count("white") == 1:
            score += 5
        elif window.count(player) == 2 and window.count("white") == 2:
            score += 2

        if window.count(opponent.color) == 3 and window.count("white") == 1:
            score -= 4

        #only AI2 will run customized EFs
        if EFmode and player.ev1_set:
            # print("using strategy 1: trying to conquer the center")
            # Conquer the center strategy: Assign higher scores to positions closer to the center - ATK
            center_col = self._cols // 2
            for i in range(4):
                if window[i] == player.color:
                    score += abs(center_col - (i + 1))  # Adjust the weight as needed
        
        if EFmode and player.ev2_set:
            # print("using strategy 2: building a 7 trap.")
            # 7-trap strategy - ATK
            # Focuses on a particular 4-piece configuration with one player's piece at each end.
            # It looks for a configuration where there is one piece of the current player (player), three empty spaces (EMPTY), and the player's pieces are at both ends of the configuration (window[0] and window[3]).
            if window.count(player.color) == 1 and window.count("white") == 3:
                # Check for a "7-trap" pattern: [X, ., ., O] or [O, ., ., X]
                if window[0] == player.color and window[3] == player.color:
                    score += 10
        
        if EFmode and player.ev3_set:
            # print("using strategy 3: evaluating surrounding discs.")
            # Evaluate surrounding discs: Check left, right, up, down, and both diagonals - ATK
            for i in range(4):
                # Check left
                if i > 0 and window[i - 1] == player.color:
                    score += 1
                # Check right
                if i < 3 and window[i + 1] == player.color:
                    score += 1
                # Check up
                if window[i] == player.color and i < 2 and window[i + 2] == player.color:
                    score += 1
                # Check down
                if window[i] == player.color and i > 1 and window[i - 2] == player.color:
                    score += 1
                # Check both diagonals
                if i % 2 == 0 and window[i] == player.color and window[(i + 2) % 4] == player.color:
                    score += 1
        if EFmode and player.ev4_set:
            # print("using strategy 4: block opponent's trap.")
            # Evaluate blocking opponent's trap - DEFENSIVE
            for i in range(2):
                if window[i] == opponent.color and window[i + 2] == opponent.color and window[i + 1] == "white" and window[(i + 3) % 4] == "white":
                    score -= 8

        if EFmode and player.ev5_set:
            # print("using strategy 5: 7 trap.")
            #7 trap again
            for i in range(2):
                if window[i] == player.color and window[i + 2] == player.color and window[i + 1] == "white" and window[(i + 3) % 4] == "white":
                    score += 10

        if EFmode and player.ev6_set:
            # Check for horizontal fork
            # print("using strategy 6: horizontal fork.")
            if window.count(player.color) == 2 and window.count("white") == 2:
                if window.count(opponent.color) == 1:
                    score += 10
            
            # Check for vertical fork
            if window.count(player.color) == 1 and window.count("white") == 3:
                if window.count(opponent.color) == 2:
                    score += 10
            
            # Check for diagonal (positive slope) fork
            if window.count(player.color) == 2 and window.count("white") == 2:
                if window.count(opponent.color) == 1:
                    score += 10
            
            # Check for diagonal (negative slope) fork
            if window.count(player.color) == 1 and window.count("white") == 3:
                if window.count(opponent.color) == 2:
                    score += 10

        return score

    def evaluate_board(self, board, EFmode):
        score = 0

        # Evaluate based on winning positions
        if self.check_winner(board, self._players[self._player_index]):
            score += 100
        elif self.check_winner(board, self._players[self._opponent_index]):
            score -= 100

        # Evaluate based on the number of computer's pieces in rows, columns, and diagonals
        for row in range(self._rows):
            for col in range(self._cols - 3):
                window = [board[row][col + i].color for i in range(4)]
                score += self.evaluate_window(window, self._players[self._player_index], EFmode)

        for col in range(self._cols):
            for row in range(self._rows - 3):
                window = [board[row + i][col].color for i in range(4)]
                score += self.evaluate_window(window, self._players[self._player_index], EFmode)

        for row in range(self._rows - 3):
            for col in range(self._cols - 3):
                window = [board[row + i][col + i].color for i in range(4)]
                score += self.evaluate_window(window, self._players[self._player_index], EFmode)

        for row in range(self._rows - 3):
            for col in range(self._cols - 3):
                window = [board[row + 3 - i][col + i].color for i in range(4)]
                score += self.evaluate_window(window, self._players[self._player_index], EFmode)

        return score
    
    def minimax(self, board, depth, is_maximizing, alpha, beta, EFmode):
        if depth == 0 or self.check_winner(board, self._players[self._opponent_index]) or self.check_winner(board, self._players[self._player_index]) or self.is_full(board):
            return self.evaluate_board(board, EFmode)

        if is_maximizing:
            max_eval = -float('inf')
            for col in range(self._cols):
                if self.is_valid_move(board, col):
                    board_copy = board_copy = [
                        [Disk(disk.screen, disk.color, disk.center, disk.width) for disk in row]  # Create a copy of each Disk object in the row
                        for row in self._disks
                    ]
                    self.make_move(board_copy, col, self._players[self._player_index])
                    eval = self.minimax(board_copy, depth - 1, False, alpha, beta, EFmode)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = float('inf')
            for col in range(self._cols):
                if self.is_valid_move(board, col):
                    board_copy = board_copy = [
                        [Disk(disk.screen, disk.color, disk.center, disk.width) for disk in row]  # Create a copy of each Disk object in the row
                        for row in self._disks
                    ]                    
                    self.make_move(board_copy, col, self._players[self._opponent_index])
                    eval = self.minimax(board_copy, depth - 1, True, alpha, beta, EFmode)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval

    def get_computer_move(self, player):
        """Use the minimax algorithm with Alpha-Beta pruning to make the computer's move"""
        columns = [col for col in range(self._cols) if self.is_valid_move(self._disks, col)]
        random.shuffle(columns)
        best_score = -float('inf')
        best_move = None

        for col in columns:
            if self.is_valid_move(self._disks, col):
                board_copy = [
                    [Disk(disk.screen, disk.color, disk.center, disk.width) for disk in row]  # Create a copy of each Disk object in the row
                    for row in self._disks
                ]
                self.make_move(board_copy, col, player)
                d = random.randint(3, 3)  # Randomly select a depth between 2 and 4
                score = self.minimax(board_copy, d, False, -float('inf'), float('inf'), player.ef_mode)  # Depth can be adjusted.

                if score > best_score:
                    best_score = score
                    best_move = col
        return best_move
    
    def run(self):
        """Process the game's events"""
        self.initialize_players()

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
            while not move_made and not self._game_over:
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
                                self.make_move(self._disks, col, current_player)

                                # move was made, change flag to true to stop current player's turn
                                move_made = True
                                    
                if not current_player.is_human: # player computer (AI)
                    col = self.get_computer_move(current_player)  # this function will calculate the best move for AI
                    self.make_move(self._disks, col, current_player)

                    # move was made, change flag to true to stop current player's turn
                    move_made = True

                if self._game_type == 0:
                    time.sleep(0.5)

                self.draw()
                self._clock.tick(self._frame_rate)
                pygame.display.update()

            # check if current player is a winner
            if self.check_winner(self._disks, self._players[self._player_index]):
                self._game_over = True
                self._game_over_popup.update_message(f"Player {self._player_index + 1} wins!")

            # check if opponent is a winner
            if self.check_winner(self._disks, self._players[self._opponent_index]):
                self._game_over = True
                self._game_over_popup.update_message(f"Player {self._opponent_index + 1} wins!")

            # check for draws (board is full)
            if self.is_full(self._disks):
                self._game_over = True
            
            while self._game_over:
                # draw the popup
                self.draw()
                pygame.display.update()

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        sys.exit(0)

                    self._game_over_popup.process_events(event)
                    
                    # exit if "Exit Game" button is pressed
                    if self._game_over_popup.buttons[0].clicked:
                        sys.exit(0)

                    # Restart the game if "Play Again" button is pressed
                    if self._game_over_popup.buttons[1].clicked:
                        self._game_over_popup.buttons[1].toggle()
                        self._new_game = True
                        self._game_over = False

            # switch players in order
            self._opponent_index = self._player_index
            self._player_index = (self._player_index + 1) % 2