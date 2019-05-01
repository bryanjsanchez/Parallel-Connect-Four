import os, time
import numpy as np

ROWS = 6
COLUMNS = 7
EMPTY = 0
HUMAN = 1
AI = 2


def create_board():
    return np.zeros((ROWS, COLUMNS), np.int8)


def place_piece(board, player, column):
    if column in range(1, 7):
        index = column - 1
        for row in reversed(range(ROWS)):
            if board[row][index] == EMPTY:
                board[row][index] = player
                return True
    return False


def draw_game(board, AI_move=0):
    highlight_index = AI_move - 1
    os.system('clear')
    print("  ____                            _     _____                ")
    print(" / ___|___  _ __  _ __   ___  ___| |_  |  ___|__  _   _ _ __ ")
    print("| |   / _ \| '_ \| '_ \ / _ \/ __| __| | |_ / _ \| | | | '__|")
    print("| |__| (_) | | | | | | |  __/ (__| |_  |  _| (_) | |_| | |   ")
    print(" \____\___/|_| |_|_| |_|\___|\___|\__| |_|  \___/ \__,_|_|\n")
    print("                     ╔═════════════════╗")
    print("                     ║   Your turn!    ║")
    print("                     ║                 ║")
    for row in board:
        line = "\033[4;30;47m|\033[0m"
        for col, piece in enumerate(row):
            if piece == HUMAN:
                if col == highlight_index:
                    highlight_index = -1
                line += "\033[4;34;47m●\033[0m"
            elif piece == AI:
                if col == highlight_index:
                    line = line[:-19] + "\033[4;31;43m|●|\033[0m"
                    highlight_index = -1
                    continue
                else:
                    line += "\033[4;31;47m●\033[0m"
            else:
                line += "\033[4;30;47m \033[0m"
            line += "\033[4;30;47m|\033[0m"
        print("                     ║ " + line + " ║")
    print("                     ║  1 2 3 4 5 6 7  ║")
    print("                     ╚═════════════════╝\n")
    print("              Type column to play or 'q' to quit\n")
    print("Next move: ")


board = create_board()
place_piece(board, HUMAN, 4)
place_piece(board, AI, 1)
place_piece(board, HUMAN, 1)
place_piece(board, AI, 2)
place_piece(board, HUMAN, 6)
place_piece(board, AI, 3)
place_piece(board, HUMAN, 4)
place_piece(board, AI, 3)
place_piece(board, HUMAN, 4)
draw_game(board)
while True:
    pressed_key = input()

    try:
        pressed_key = int(pressed_key)
    except ValueError:
        pass

    if pressed_key in range(1,8):
        print("\nWaiting for opponent...")
        time.sleep(1)
        draw_game(board, pressed_key)
    elif pressed_key == "q":
        os.system("clear")
        print("\nThank you for playing!")
        exit()
    else:
        print("\nInvalid input, try again...")
        time.sleep(1)
        pressed_key = 0
        draw_game(board, pressed_key)
