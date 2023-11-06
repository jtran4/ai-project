import random
from collections import deque

# Define constants for the game board dimensions
BOARD_SIZE = 6

# Initialize the game board
board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Define the player and obstacle symbols
mouse_symbol = 'M'
cat_symbol = 'C'
cheese_symbol = 'Cheese'
trap_symbol = 'Trap'

# Place the mouse and cat on the board
mouse_position = (0, random.randint(0, BOARD_SIZE - 1))
cat_position = (BOARD_SIZE - 1, random.randint(0, BOARD_SIZE - 1))

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

# Function to display the game board
def display_board(board):
    cell_width = max(len(cheese_symbol), len(cat_symbol), len(mouse_symbol), len(trap_symbol)) + 2
    horizontal_line = '+'.join(['-' * cell_width] * BOARD_SIZE)

    # Display column numbers starting from 1
    column_numbers = ' ' * cell_width
    for i in range(1, BOARD_SIZE + 1):
        column_numbers += f'{i:^{cell_width}}'

    print(column_numbers)

    for row_index, row in enumerate(board):
        print(horizontal_line)
        print(f'{row_index + 1:^{cell_width}}|' + '|'.join([f'{cell:^{cell_width}}' for cell in row]) + '|')

    print(horizontal_line)

# Function to move the mouse or cat
def move_piece(board, position, new_position, symbol):
    x, y = position
    new_x, new_y = new_position
    board[x][y] = ' '
    board[new_x][new_y] = symbol
    return new_position

# Function to find the cat's next move using BFS
def find_cat_move(board, cat_pos, mouse_pos):
    queue = deque([(cat_pos, [])])
    visited = set()

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == mouse_pos:
            return path

        visited.add((x, y))

        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            new_x, new_y = x + dx, y + dy
            if 0 <= new_x < BOARD_SIZE and 0 <= new_y < BOARD_SIZE and board[new_x][new_y] != trap_symbol and (new_x, new_y) not in visited:
                queue.append(((new_x, new_y), path + [(new_x, new_y)]))

# Main game loop
trap_disabled = False
move_counter = 0  # Counter to keep track of the mouse's movement

while True:
    display_board(board)

    if not trap_disabled:
        move = input("Enter 'w' (up), 's' (down), 'a' (left), 'd' (right) to move the mouse: ")
    else:
        move = input("The mouse is trapped! Enter any key to skip a turn: ")

    if move == 'w':
        if mouse_position[0] > 0 and not trap_disabled:
            mouse_position = move_piece(board, mouse_position, (mouse_position[0] - 1, mouse_position[1]), mouse_symbol)
    elif move == 's':
        if mouse_position[0] < BOARD_SIZE - 1 and not trap_disabled:
            mouse_position = move_piece(board, mouse_position, (mouse_position[0] + 1, mouse_position[1]), mouse_symbol)
    elif move == 'a':
        if mouse_position[1] > 0 and not trap_disabled:
            mouse_position = move_piece(board, mouse_position, (mouse_position[0], mouse_position[1] - 1), mouse_symbol)
    elif move == 'd':
        if mouse_position[1] < BOARD_SIZE - 1 and not trap_disabled:
            mouse_position = move_piece(board, mouse_position, (mouse_position[0], mouse_position[1] + 1), mouse_symbol)

    # Implement cat's movement and game logic here
    cat_move = find_cat_move(board, cat_position, mouse_position)
    if cat_move:
        cat_position = move_piece(board, cat_position, cat_move[0], cat_symbol)

    # Check for game over conditions and break the loop if needed
    if cat_position == mouse_position:
        print("Cat caught the mouse! Game over.")
        break

    # Check for trap activation
    if move_counter % 2 == 0:
        trap_disabled = False
    else:
        trap_disabled = True

    # Check for cheese and allow double movement
    if board[mouse_position[0]][mouse_position[1]] == cheese_symbol:
        move_counter += 1












