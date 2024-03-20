import random
import os
import string

alphabet = list(string.ascii_uppercase)

os.environ['TERM'] = 'xterm-256color'

BOMB = 9

welcome = """
███╗   ███╗██╗███╗   ██╗███████╗███████╗██╗    ██╗███████╗███████╗██████╗ ███████╗██████╗ 
████╗ ████║██║████╗  ██║██╔════╝██╔════╝██║    ██║██╔════╝██╔════╝██╔══██╗██╔════╝██╔══██╗
██╔████╔██║██║██╔██╗ ██║█████╗  ███████╗██║ █╗ ██║█████╗  █████╗  ██████╔╝█████╗  ██████╔╝
██║╚██╔╝██║██║██║╚██╗██║██╔══╝  ╚════██║██║███╗██║██╔══╝  ██╔══╝  ██╔═══╝ ██╔══╝  ██╔══██╗
██║ ╚═╝ ██║██║██║ ╚████║███████╗███████║╚███╔███╔╝███████╗███████╗██║     ███████╗██║  ██║
╚═╝     ╚═╝╚═╝╚═╝  ╚═══╝╚══════╝╚══════╝ ╚══╝╚══╝ ╚══════╝╚══════╝╚═╝     ╚══════╝╚═╝  ╚═╝
"""


def get_board_size():
    while True:
        try:
            size = int(input("Please enter the size of the board (a number between 2 and 26): "))
            if 2 <= size <= 26:
                return size
            else:
                print("Size must be between 2 and 26.")
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def create_board():
    board = initialize_board(SIZE)
    return board


def initialize_board(size):
    return [[0] * size for _ in range(size)]


def set_up_board():
    place_bombs(BOMBS_IN_GAME)
    add_markers()


def calculate_bombs(board_size):
    default_size = 10
    default_bombs = 13

    default_cells = default_size * default_size

    bomb_density = default_bombs / default_cells

    user_cells = board_size * board_size

    bombs = round(bomb_density * user_cells)

    return bombs


def place_bombs(number_of_bombs):
    bomb_positions = random.sample([(i, j) for i in range(len(game_board))
                                    for j in range(len(game_board[0]))], number_of_bombs)

    for column, row in bomb_positions:
        game_board[column][row] = BOMB


def add_markers():
    for i in range(len(game_board)):
        for j in range(len(game_board[0])):
            if game_board[i][j] != BOMB:
                bombs_around = count_bombs(i, j)
                game_board[i][j] = bombs_around


def count_bombs(column, row):
    """
     Count the number of bombs surrounding the specified cell.

     Parameters:
     - game_board (list of lists): The game board representing the minesweeper grid.
     - column (int): The column index of the specified cell.
     - row (int): The row index of the specified cell.

     Returns:
     - result (int): The number of bombs surrounding the specified cell.
     """

    result = 0
    rows, cols = len(game_board), len(game_board[0])

    for i in range(max(0, column - 1), min(rows, column + 2)):
        for j in range(max(0, row - 1), min(cols, row + 2)):
            if game_board[i][j] == BOMB:
                result += 1

    return result


def play_game():
    revealed_cells = []
    flagged_cells = []
    game_won = True

    while len(revealed_cells) != (SIZE * SIZE) - BOMBS_IN_GAME:
        clear_and_draw_board(revealed_cells, flagged_cells)

        action = input("\nEnter 'r' to reveal, 'f' to flag, or 'u' to unflag: ")
        if action.lower() == 'r':
            column, row = get_user_input()
            selected_cell = [column, row]

            if selected_cell in revealed_cells:
                continue

            if game_board[column][row] == BOMB:
                revealed_cells.append(selected_cell)
                game_won = False
                break
            else:
                revealed_cells = reveal_cells(revealed_cells, column, row)
        elif action.lower() == 'f':
            column, row = get_user_input()
            flagged_cells.append([column, row])
        elif action.lower() == 'u':
            column, row = get_user_input()
            if [column, row] in flagged_cells:
                flagged_cells.remove([column, row])

    clear_and_draw_board(revealed_cells, flagged_cells, game_over=True)

    if game_won:
        print("\nYou win! Congratulations.")
    else:
        print("\nYou lose! Try again.")


def get_user_input():
    user_input = input("Enter coordinates (e.g., '5A', '10C', '54F'): ")

    # Split the input into row and column parts
    row_input = ""
    column_input = ""
    for char in user_input:
        if char.isdigit():
            column_input += char
        else:
            row_input += char

    # Convert the row input to an integer and adjust for zero-based indexing
    column = int(column_input) - 1

    # Validate column input
    if len(row_input) != 1 or row_input.upper() not in alphabet:
        print("Invalid input. Please enter valid column (e.g., 'A', 'B', 'C', etc.).")
        return get_user_input()

    # Convert column input to column index
    row = alphabet.index(row_input.upper())

    # Validate row and column indexes
    if not check_indexes(column, row):
        print("Invalid coordinates. Please enter coordinates within the board size.")
        return get_user_input()

    return column, row


def draw_board(revealed_cells, flagged_cells, game_over=False):
    print(welcome)

    print(f"{BOMBS_IN_GAME - len(flagged_cells)} bombs left.\n")

    col_indices = "X\Y  " + " ".join(f"{alphabet[i]: <3}" for i in range(len(game_board[0])))
    print(col_indices)

    for i in range(len(game_board)):
        print("   " + "-" * (len(game_board) * 4 + 1))
        row = f"{i + 1: <2} | "  # Display row number starting from 1
        for j in range(len(game_board[i])):
            if game_over:
                if game_board[i][j] == BOMB:
                    row += "X | "
                else:
                    row += f"{game_board[i][j]: <2}| "
            elif [i, j] in revealed_cells:
                if game_board[i][j] == BOMB:
                    row += "X | "
                else:
                    row += f"{game_board[i][j]: <2}| "
            elif [i, j] in flagged_cells:
                row += "F | "
            else:
                row += "  | "
        print(row)

    print("   " + "-" * (len(game_board) * 4 + 1))


def clear_and_draw_board(revealed_cells, flagged_cells, game_over=False):
    clear_console()
    draw_board(revealed_cells, flagged_cells, game_over)


def check_indexes(column, row):
    return 0 <= column < len(game_board) and 0 <= row < len(game_board)


def reveal_cells(revealed_cells, column, row):
    """
        Recursively reveal cells on the game board based on the selected cell (column, row)
        and update the list of revealed cells.

        Parameters:
        - game_board (list of lists): The game board representing the minesweeper grid.
        - revealed_cells (list of lists): The list of cells that have been revealed.
        - column (int): The row index of the selected cell.
        - row (int): The column index of the selected cell.

        Returns:
        - revealed_cells (list of lists): The updated list of revealed cells after revealing adjacent cells.
    """

    if [column, row] not in revealed_cells:
        revealed_cells.append([column, row])

        if game_board[column][row] == 0:
            rows, cols = len(game_board), len(game_board[0])

            for i in range(max(0, column - 1), min(rows, column + 2)):
                for j in range(max(0, row - 1), min(cols, row + 2)):
                    revealed_cells = reveal_cells(revealed_cells, i, j)

    return revealed_cells


def clear_console():
    os.system('cls' if os.name == 'nt' else 'clear')


if __name__ == "__main__":
    print(welcome)

    SIZE = get_board_size()
    BOMBS_IN_GAME = calculate_bombs(SIZE)

    game_board = create_board()

    set_up_board()

    play_game()
