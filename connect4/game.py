import numpy as np
import random

# Constants for the game
EMPTY = 0
PLAYER = 1
COMPUTER = 2
ROWS = 6        #this value could be customized
COLS = 7        #this value could be customized
CONNECT = 4     #this value could be customized

# Initialize the game board
board = np.zeros((ROWS, COLS), dtype=int)

# Initialize win counters
player_wins = 0
computer_wins = 0
draws = 0

# Function to load win counts from a file
def load_win_counts():
    try:
        with open("win_counts.txt", "r") as file:
            data = file.read().split(",")
            return int(data[0]), int(data[1]), int(data[2])
    except FileNotFoundError:
        return 0, 0, 0

# Function to save win counts to a file
def save_win_counts(player_wins, computer_wins, draws):
    with open("win_counts.txt", "w") as file:
        file.write(f"{player_wins},{computer_wins},{draws}")

# Load win counts at the beginning of the program
player_wins, computer_wins, draws = load_win_counts()

def print_board(board):
    print("")
    for row in board:
        print(' '.join(['O' if cell == PLAYER else 'X' if cell == COMPUTER else '.' for cell in row]))
    board_number = "1"
    for x in range(2, COLS + 1):
        board_number = board_number + " " + str(x)
    print(board_number)
    #print('1 2 3 4 5 6 7')

def is_valid_move(board, col):
    return board[0][col] == EMPTY

def make_move(board, col, player):
    for row in range(ROWS - 1, -1, -1):
        if board[row][col] == EMPTY:
            board[row][col] = player
            break

def check_winner(board, player):
    for row in range(ROWS):
        for col in range(COLS):
            if board[row][col] == player:
                # Check horizontally
                if col + CONNECT <= COLS and all(board[row][col+i] == player for i in range(CONNECT)):
                    return True
                # Check vertically
                if row + CONNECT <= ROWS and all(board[row+i][col] == player for i in range(CONNECT)):
                    return True
                # Check diagonally (positive slope)
                if col + CONNECT <= COLS and row + CONNECT <= ROWS and all(board[row+i][col+i] == player for i in range(CONNECT)):
                    return True
                # Check diagonally (negative slope)
                if col - CONNECT + 1 >= 0 and row + CONNECT <= ROWS and all(board[row+i][col-i] == player for i in range(CONNECT)):
                    return True
    return False

def is_full(board):
    return all(cell != EMPTY for cell in board[0])

def get_player_move():
    # Use the minimax algorithm with Alpha-Beta pruning to make the computer's move.
    if gameMode == 0:
        #print("AI vs AI mode")
        #columns = list(range(COLS))
        columns = [col for col in range(COLS) if is_valid_move(board, col)]
        random.shuffle(columns)
        best_score = -float('inf')
        best_move = None
        #for col in range(COLS):
        for col in columns:
            if is_valid_move(board, col):
                board_copy = board.copy()
                make_move(board_copy, col, COMPUTER)
                d = random.randint(3, 3)  # Randomly select a depth between 2 and 4
                score = minimax(board_copy, d, False, -float('inf'), float('inf'), 0)  # Depth can be adjusted.
                if score > best_score:
                    best_score = score
                    best_move = col
        return best_move
    else:
        #print("Player vs AI mode")
        while True:
            try:
                col = int(input("Enter your move (1-" + str(COLS) + "): ")) - 1
                if col >= 0 and col < COLS and is_valid_move(board, col):
                    return col
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Please enter a number between 1 and 7.")



def get_computer_move(board):
    # Use the minimax algorithm with Alpha-Beta pruning to make the computer's move.
    #columns = list(range(COLS))
    columns = [col for col in range(COLS) if is_valid_move(board, col)]
    random.shuffle(columns)
    best_score = -float('inf')
    best_move = None
    #for col in range(COLS):
    for col in columns:
        if is_valid_move(board, col):
            board_copy = board.copy()
            make_move(board_copy, col, COMPUTER)
            d = random.randint(3, 3)  # Randomly select a depth between 2 and 4
            score = minimax(board_copy, d, False, -float('inf'), float('inf'), evalFuncMode)  # Depth can be adjusted.

            if score > best_score:
                best_score = score
                best_move = col
    return best_move

def minimax(board, depth, is_maximizing, alpha, beta, EFmode):
    #print(EFmode)
    if depth == 0 or check_winner(board, PLAYER) or check_winner(board, COMPUTER) or is_full(board):
        return evaluate_board(board, EFmode)

    if is_maximizing:
        max_eval = -float('inf')
        for col in range(COLS):
            if is_valid_move(board, col):
                board_copy = board.copy()
                make_move(board_copy, col, COMPUTER)
                eval = minimax(board_copy, depth - 1, False, alpha, beta, EFmode)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
        return max_eval
    else:
        min_eval = float('inf')
        for col in range(COLS):
            if is_valid_move(board, col):
                board_copy = board.copy()
                make_move(board_copy, col, PLAYER)
                eval = minimax(board_copy, depth - 1, True, alpha, beta, EFmode)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

def evaluate_board(board, EFmode):
    #if evalFuncMode == 0:
        #print("using strategy 0: no traps")
        score = 0

        # Evaluate based on winning positions
        if check_winner(board, COMPUTER):
            score += 100
        elif check_winner(board, PLAYER):
            score -= 100

        # Evaluate based on the number of computer's pieces in rows, columns, and diagonals
        for row in range(ROWS):
            for col in range(COLS - 3):
                window = [board[row][col + i] for i in range(4)]
                score += evaluate_window(window, COMPUTER, EFmode)

        for col in range(COLS):
            for row in range(ROWS - 3):
                window = [board[row + i][col] for i in range(4)]
                score += evaluate_window(window, COMPUTER, EFmode)

        for row in range(ROWS - 3):
            for col in range(COLS - 3):
                window = [board[row + i][col + i] for i in range(4)]
                score += evaluate_window(window, COMPUTER, EFmode)

        for row in range(ROWS - 3):
            for col in range(COLS - 3):
                window = [board[row + 3 - i][col + i] for i in range(4)]
                score += evaluate_window(window, COMPUTER, EFmode)

        return score
    #if evalFuncMode == 1:
    #    print("using strategy 1: trying to conquer the center")
    #if evalFuncMode == 2:
    #    print("using strategy 2: building a 7 trap.")
    #if evalFuncMode == 3:
    #    print("using strategy 3: evaluating surrounding discs.")


def evaluate_window(window, player, EFmode):
    score = 0
    opponent = PLAYER if player == COMPUTER else COMPUTER

    if window.count(player) == 4:
        score += 100
    elif window.count(player) == 3 and window.count(EMPTY) == 1:
        score += 5
    elif window.count(player) == 2 and window.count(EMPTY) == 2:
        score += 2

    if window.count(opponent) == 3 and window.count(EMPTY) == 1:
        score -= 4

    if EFmode == 1 or EFmode == -2:
        #print("using strategy 1: trying to conquer the center")
        # Conquer the center strategy: Assign higher scores to positions closer to the center - ATK
        center_col = COLS // 2
        for i in range(4):
            if window[i] == player:
                score += abs(center_col - (i + 1))  # Adjust the weight as needed
    
    if EFmode == 2 or EFmode == -1:
        #print("using strategy 2: building a 7 trap.")
        # 7-trap strategy - ATK
        if window.count(player) == 1 and window.count(EMPTY) == 3:
            # Check for a "7-trap" pattern: [X, ., ., O] or [O, ., ., X]
            if window[0] == player and window[3] == player:
                score += 10
    
    if EFmode == 3 or EFmode == -2:
        #print("using strategy 3: evaluating surrounding discs.")
        # Evaluate surrounding discs: Check left, right, up, down, and both diagonals - ATK
        for i in range(4):
            # Check left
            if i > 0 and window[i - 1] == player:
                score += 1
            # Check right
            if i < 3 and window[i + 1] == player:
                score += 1
            # Check up
            if window[i] == player and i < 2 and window[i + 2] == player:
                score += 1
            # Check down
            if window[i] == player and i > 1 and window[i - 2] == player:
                score += 1
            # Check both diagonals
            if i % 2 == 0 and window[i] == player and window[(i + 2) % 4] == player:
                score += 1
    if EFmode == 4 or EFmode == -2:
        # Evaluate blocking opponent's trap - DEFENSIVE
        for i in range(2):
            if window[i] == opponent and window[i + 2] == opponent and window[i + 1] == EMPTY and window[(i + 3) % 4] == EMPTY:
                score -= 8

    if EFmode == 5 or EFmode == -1:
        #7 trap again
        for i in range(2):
            if window[i] == player and window[i + 2] == player and window[i + 1] == EMPTY and window[(i + 3) % 4] == EMPTY:
                score += 10

    if EFmode == 6 or EFmode == -2:
         # Check for horizontal fork
        if window.count(player) == 2 and window.count(EMPTY) == 2:
            if window.count(opponent) == 1:
                score += 10
        
        # Check for vertical fork
        if window.count(player) == 1 and window.count(EMPTY) == 3:
            if window.count(opponent) == 2:
                score += 10
        
        # Check for diagonal (positive slope) fork
        if window.count(player) == 2 and window.count(EMPTY) == 2:
            if window.count(opponent) == 1:
                score += 10
        
        # Check for diagonal (negative slope) fork
        if window.count(player) == 1 and window.count(EMPTY) == 3:
            if window.count(opponent) == 2:
                score += 10

    return score



def main():
    print("Welcome to Connect Four!")
    player_turn = True
    global player_wins, computer_wins, draws
    
    #evalFuncMode 0 = default, 1 = center, 2 = seven trap, 3 = surrounding, 
    global evalFuncMode
    evalFuncMode = -1

    #game mode 0 = AI vs AI, mode 1 = player vs AI
    global gameMode
    gameMode = 0
    while True:
        if gameMode == 1:
            print_board(board)

        if player_turn:
            col = get_player_move()     # this function will calculate the best move for p1
            make_move(board, col, PLAYER)
            if gameMode == 1:
                print('Player movement: ' + str(col+1))
            if check_winner(board, PLAYER):
                print_board(board)
                if gameMode == 1:
                    print("Player wins!")
                else:
                    print("AI (default) wins!")
                player_wins += 1
                #save_win_counts(player_wins, computer_wins, draws)  # Save win counts to a file
                #print('score: Player: ' + str(player_wins) + '\tAI: ' + str(computer_wins) + '\tDraws: ' + str(draws))
                break
        else:
            col = get_computer_move(board)  #this function will calculate the best move for p2
            make_move(board, col, COMPUTER)
            if gameMode == 1:
                print('AI movement: ' + str(col+1))
            if check_winner(board, COMPUTER):
                print_board(board)
                if gameMode == 1:
                    print("AI wins!")
                else:
                    print("AI (customized) wins!")
                computer_wins += 1
                #save_win_counts(player_wins, computer_wins, draws)
                #print('score: Player: ' + str(player_wins) + '\tAI: ' + str(computer_wins) + '\tDraws: ' + str(draws))
                break

        if is_full(board):
            print_board(board)
            print("It's a draw!") 
            draws += 1
            #save_win_counts(player_wins, computer_wins, draws)
            #print('score: Player: ' + str(player_wins) + '\tAI: ' + str(computer_wins) + '\tDraws: ' + str(draws))
            break

        player_turn = not player_turn

    save_win_counts(player_wins, computer_wins, draws)  # Save win counts to a file
    if gameMode == 1:
        print('score: Player: ' + str(player_wins) + '\tAI: ' + str(computer_wins) + '\tDraws: ' + str(draws))
    else:
        print('score: AI(default): ' + str(player_wins) + '\tAI(customized): ' + str(computer_wins) + '\tDraws: ' + str(draws))
if __name__ == "__main__":
    main()

