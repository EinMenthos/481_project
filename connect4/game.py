import numpy as np

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
    best_score = -float('inf')
    best_move = None
    for col in range(COLS):
        if is_valid_move(board, col):
            board_copy = board.copy()
            make_move(board_copy, col, COMPUTER)
            score = minimax(board_copy, 3, False, -float('inf'), float('inf'))  # Depth can be adjusted.

            if score > best_score:
                best_score = score
                best_move = col

    return best_move

def minimax(board, depth, is_maximizing, alpha, beta):
    if depth == 0 or check_winner(board, PLAYER) or check_winner(board, COMPUTER) or is_full(board):
        return evaluate_board(board)

    if is_maximizing:
        max_eval = -float('inf')
        for col in range(COLS):
            if is_valid_move(board, col):
                board_copy = board.copy()
                make_move(board_copy, col, COMPUTER)
                eval = minimax(board_copy, depth - 1, False, alpha, beta)
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
                eval = minimax(board_copy, depth - 1, True, alpha, beta)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
        return min_eval

def evaluate_board(board):
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
            score += evaluate_window(window, COMPUTER)

    for col in range(COLS):
        for row in range(ROWS - 3):
            window = [board[row + i][col] for i in range(4)]
            score += evaluate_window(window, COMPUTER)

    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = [board[row + i][col + i] for i in range(4)]
            score += evaluate_window(window, COMPUTER)

    for row in range(ROWS - 3):
        for col in range(COLS - 3):
            window = [board[row + 3 - i][col + i] for i in range(4)]
            score += evaluate_window(window, COMPUTER)

    return score

def evaluate_window(window, player):
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

    return score


def main():
    print("Welcome to Connect Four!")
    player_turn = True
    global player_wins, computer_wins, draws

    while True:
        print_board(board)

        if player_turn:
            col = get_player_move()
            make_move(board, col, PLAYER)
            print('player movement: ' + str(col+1))
            if check_winner(board, PLAYER):
                print_board(board)
                print("Player wins!")
                player_wins += 1
                save_win_counts(player_wins, computer_wins, draws)  # Save win counts to a file
                print('score: Player: ' + str(player_wins) + '\tAI: ' + str(computer_wins) + '\tDraws: ' + str(draws))
                break
        else:
            col = get_computer_move(board)
            make_move(board, col, COMPUTER)
            print('CPU movement: ' + str(col+1))
            if check_winner(board, COMPUTER):
                print_board(board)
                print("Computer wins!")
                computer_wins += 1
                save_win_counts(player_wins, computer_wins, draws)
                print('score: Player: ' + str(player_wins) + '\tAI: ' + str(computer_wins) + '\tDraws: ' + str(draws))
                break

        if is_full(board):
            print_board(board)
            print("It's a draw!") 
            draws += 1
            save_win_counts(player_wins, computer_wins, draws)
            print('score: Player: ' + str(player_wins) + '\tAI: ' + str(computer_wins) + '\tDraws: ' + str(draws))
            break

        player_turn = not player_turn

if __name__ == "__main__":
    main()
