import random
from collections import deque
import time
import os

# Define constants for the game board dimensions
BOARD_SIZE = 6

# Clear the screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Animated title screen
def generate_title_screen():
    title = """
      \    /\                                                                                           *
       )  ( ') 
      (  /  )       __QQ
       \(__)|      (_)_">
   ____      _    _)                  _       __  __                         ____                      _ 
  / ___|__ _| |_       __ _ _ __   __| |     |  \/  | ___  _   _ ___  ___   / ___| __ _ _ __ ___   ___| |
 | |   / _` | __|____ / _` | '_ \ / _` |_____| |\/| |/ _ \| | | / __|/ _ \ | |  _ / _` | '_ ` _ \ / _ \ |
 | |__| (_| | ||_____| (_| | | | | (_| |_____| |  | | (_) | |_| \__ \  __/ | |_| | (_| | | | | | |  __/_|
  \____\__,_|\__|     \__,_|_| |_|\__,_|     |_|  |_|\___/ \__,_|___/\___|  \____|\__,_|_| |_| |_|\___(_)
    
"""

    print(title)
    # Generate title screen
    load_message = "LOADING GAME..."
    for letter in load_message:
        print(letter, end='', flush=True)
        time.sleep(0.1)  # Adjust the delay as needed
    print("\n")

# Select game mode
def select_game_mode():
    while True:
        clear_screen()
        generate_title_screen()
        game_mode = input("Select game mode (single-player or multiplayer): ").lower()
        if game_mode in ['single-player', 'multiplayer']:
            return game_mode
        else:
            print("Invalid game mode. Please choose either 'single-player' or 'multiplayer'.")
            time.sleep(2)

# Initialize the game board
board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Define the player and obstacle symbols
mouse_symbol = 'MOUSE'
cat_symbol = 'CAT'
cheese_symbol = 'cheese'
trap_symbol = 'trap'

# Select game mode
game_mode = select_game_mode()

# Place the mouse and cat on the board based on the selected mode
if game_mode == 'single-player':
    # Place the mouse and cat such that they do not start on the same space as cheese or trap
    while True:
        mouse_position = (0, random.randint(0, BOARD_SIZE - 1))
        cat_position = (BOARD_SIZE - 1, random.randint(0, BOARD_SIZE - 1))
        if (
            board[mouse_position[0]][mouse_position[1]] == ' ' and
            board[cat_position[0]][cat_position[1]] == ' ' and
            board[mouse_position[0]][mouse_position[1]] != cheese_symbol and
            board[cat_position[0]][cat_position[1]] != trap_symbol
        ):
            break

    board[mouse_position[0]][mouse_position[1]] = mouse_symbol
    board[cat_position[0]][cat_position[1]] = cat_symbol

elif game_mode == 'multiplayer':
    # In multiplayer mode, player 1 controls the mouse and player 2 controls the cat
    while True:
        mouse_position = (0, random.randint(0, BOARD_SIZE - 1))
        cat_position = (BOARD_SIZE - 1, random.randint(0, BOARD_SIZE - 1))
        if (
            board[mouse_position[0]][mouse_position[1]] == ' ' and
            board[cat_position[0]][cat_position[1]] == ' ' and
            board[mouse_position[0]][mouse_position[1]] != cheese_symbol and
            board[cat_position[0]][cat_position[1]] != trap_symbol
        ):
            break

    board[mouse_position[0]][mouse_position[1]] = mouse_symbol
    board[cat_position[0]][cat_position[1]] = cat_symbol


# Place cheese and traps randomly on the board
num_cheese = random.randint(1, 3)
num_traps = random.randint(1, 3)

for _ in range(num_cheese):
    x, y = random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)
    board[x][y] = cheese_symbol

for _ in range(num_traps):
    x, y = random.randint(0, BOARD_SIZE - 1), random.randint(0, BOARD_SIZE - 1)
    board[x][y] = trap_symbol

# Prompt for difficulty (only applicable in single-player mode)
difficulty = None
if game_mode == 'single-player':
    difficulty = input("Select difficulty: 'easy', 'medium', or 'hard': ")
    if difficulty.lower() not in ['easy', 'medium', 'hard']:
        print("Invalid difficulty. Defaulting to easy.")
        difficulty = 'easy'

# Function to display the game board
def display_board(board):
    cell_width = max(len(cheese_symbol), len(cat_symbol), len(mouse_symbol), len(trap_symbol)) + 2
    horizontal_line = '+'.join(['-' * cell_width] * (BOARD_SIZE + 1))

    # lines for column numbers and horizontal line
    print("        |   1    |   2    |   3    |   4    |   5    |   6    |")
    print(horizontal_line)
    # Print the rows
    for row_index, row in enumerate(board):
        print(f'{row_index + 1:^{cell_width}}|' + '|'.join([f'{cell:^{cell_width}}' for cell in row]) + '|')

        if row_index < BOARD_SIZE - 1:
            print(horizontal_line)

    print("\n")


# Function to move a piece on the board
def move_piece(board, position, new_position, symbol):
    x, y = position
    new_x, new_y = new_position
    board[x][y] = ' '
    board[new_x][new_y] = symbol
    return new_position

# Function to find the cat's next move using a rule-based approach
def find_cat_move(board, cat_pos, mouse_pos, difficulty='easy'):
    def dfs(current_pos, path):
        if current_pos == mouse_pos:
            return path[0] if path else None

        visited.add(current_pos)

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = current_pos[0] + dx, current_pos[1] + dy
            if 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE and board[new_x][new_y] != trap_symbol and (new_x, new_y) not in visited:
                result = dfs((new_x, new_y), path + [(new_x, new_y)])
                if result:
                    return result

        return None

    if difficulty == 'easy':
        # Random move for easy difficulty
        possible_moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random_move = random.choice(possible_moves)
        new_position = tuple(map(sum, zip(cat_pos, random_move)))

        # Ensure the new position is within the board boundaries
        new_x, new_y = new_position
        if 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE:
            return new_position
        else:
            # If the new position is outside the board boundaries, try again
            return find_cat_move(board, cat_pos, mouse_pos, difficulty)

    elif difficulty == 'medium':
        # Use DFS for medium difficulty with random move
        possible_moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        random_move = random.choice(possible_moves)
        new_position = tuple(map(sum, zip(cat_pos, random_move)))

        # Ensure the new position is within the board boundaries
        new_x, new_y = new_position
        if 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE:
            return new_position
        else:
            # If the new position is outside the board boundaries, try again
            return find_cat_move(board, cat_pos, mouse_pos, difficulty)

    elif difficulty == 'hard':
        # Use BFS to find the optimal move for hard difficulty
        queue = deque([(cat_pos, [])])
        visited = set()

        while queue:
            (x, y), path = queue.popleft()
            if (x, y) == mouse_pos:
                return path[0] if path else None

            visited.add((x, y))

            for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
                new_x, new_y = x + dx, y + dy
                if 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE and board[new_x][new_y] != trap_symbol and (new_x, new_y) not in visited:
                    queue.append(((new_x, new_y), path + [(new_x, new_y)]))
        return None

# Function to move the cat manually (only applicable in multiplayer mode)
def move_cat_manually(board, cat_position):
    cat_move = input("Player 2 (cat), use arrow keys for movement: ")
    if cat_move == '\x1b[A':  # Up arrow key
        if cat_position[0] > 0:
            cat_position = move_piece(board, cat_position, (cat_position[0] - 1, cat_position[1]), cat_symbol)
    elif cat_move == '\x1b[B':  # Down arrow key
        if cat_position[0] < BOARD_SIZE - 1:
            cat_position = move_piece(board, cat_position, (cat_position[0] + 1, cat_position[1]), cat_symbol)
    elif cat_move == '\x1b[D':  # Left arrow key
        if cat_position[1] > 0:
            cat_position = move_piece(board, cat_position, (cat_position[0], cat_position[1] - 1), cat_symbol)
    elif cat_move == '\x1b[C':  # Right arrow key
        if cat_position[1] < BOARD_SIZE - 1:
            cat_position = move_piece(board, cat_position, (cat_position[0], cat_position[1] + 1), cat_symbol)
    return cat_position

# Main game loop
move_counter = 0  # Counter to keep track of the mouse's movement

while True:
    display_board(board)

    # Player 1 (mouse) move
    move = input("Player 1 (mouse), use 'w' (up), 's' (down), 'a' (left), 'd' (right) to move: ")
    if move.lower() == 'quit':
        print("Game ended by user.")
        break
    elif move in ['w', 's', 'a', 'd']:
        new_position = (mouse_position[0] - 1, mouse_position[1]) if move == 'w' else \
                       (mouse_position[0] + 1, mouse_position[1]) if move == 's' else \
                       (mouse_position[0], mouse_position[1] - 1) if move == 'a' else \
                       (mouse_position[0], mouse_position[1] + 1)  # 'd'
        if 0 <= new_position[0] < BOARD_SIZE and 0 <= new_position[1] < BOARD_SIZE:
            mouse_position = move_piece(board, mouse_position, new_position, mouse_symbol)

    display_board(board)  # Display the board after player 1's move

    # Check for game over conditions after player 1's move
    if cat_position == mouse_position:
        print("Cat caught the mouse! Game over.")
        break

    if mouse_position[0] == BOARD_SIZE - 1:
        print("Mouse reached the bottom! Mouse wins the game.")
        break

    # Player 2 (cat) move (only applicable in single-player mode)
    if game_mode == 'single-player':
        print("\nComputer cat's turn:")  # Print this line for the machine cat's turn
        # In single-player mode, the cat is controlled by the machine
        cat_move = find_cat_move(board, cat_position, mouse_position, difficulty)
        if cat_move:
            cat_position = move_piece(board, cat_position, cat_move, cat_symbol)

        display_board(board)  # Display the board after player 2's move (machine's turn)

        # Check for game over conditions after player 2's move
        if cat_position == mouse_position:
            print("Cat caught the mouse! Game over.")
            break

        if mouse_position[0] == BOARD_SIZE - 1:
            print("Mouse reached the bottom! Mouse wins the game.")
            break

        # Check for trap activation
        if move_counter % 2 == 0:
            trap_disabled = False
        else:
            trap_disabled = True

        # Check for cheese and allow double movement
        if board[mouse_position[0]][mouse_position[1]] == cheese_symbol:
            move_counter += 1

        # Increment the move counter for the next turn
        move_counter += 1

    # In multiplayer mode, player 2 (cat) will take a turn in the next iteration of the loop
    else:
        # Player 2 (cat) move (only applicable in multiplayer mode)
        cat_move = input("Player 2 (cat), use arrow keys for movement: ")
        if cat_move == '\x1b[A':  # Up arrow key
            if cat_position[0] > 0:
                cat_position = move_piece(board, cat_position, (cat_position[0] - 1, cat_position[1]), cat_symbol)
        elif cat_move == '\x1b[B':  # Down arrow key
            if cat_position[0] < BOARD_SIZE - 1:
                cat_position = move_piece(board, cat_position, (cat_position[0] + 1, cat_position[1]), cat_symbol)
        elif cat_move == '\x1b[D':  # Left arrow key
            if cat_position[1] > 0:
                cat_position = move_piece(board, cat_position, (cat_position[0], cat_position[1] - 1), cat_symbol)
        elif cat_move == '\x1b[C':  # Right arrow key
            if cat_position[1] < BOARD_SIZE - 1:
                cat_position = move_piece(board, cat_position, (cat_position[0], cat_position[1] + 1), cat_symbol)

        display_board(board)  # Display the board after player 2's move

        # Check for game over conditions after player 2's move
        if cat_position == mouse_position:
            print("Cat caught the mouse! Player 2 wins the game.")
            break

        if mouse_position[0] == BOARD_SIZE - 1:
            print("Mouse reached the bottom! Player 1 wins the game.")
            break

        # Check for trap activation
        if move_counter % 2 == 0:
            trap_disabled = False
        else:
            trap_disabled = True

        # Check for cheese and allow double movement
        if board[mouse_position[0]][mouse_position[1]] == cheese_symbol:
            move_counter += 1

        # Increment the move counter for the next turn
        move_counter += 1
