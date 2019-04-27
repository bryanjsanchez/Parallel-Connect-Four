import os
import numpy as np

ROWS = 6
COLUMNS = 7
EMPTY = 0
HUMAN = 1
AI = 2


def create_board():
    return np.zeros((ROWS, COLUMNS), np.int8)


def place_piece(board, player, col):
    if col < 0 or col >= COLUMNS:
        raise ValueError("Invalid column")
    for row in reversed(range(ROWS)):
        if board[row][col] == EMPTY:
            board[row][col] = player
            return
    raise ValueError("Column is full")


def display(board):
    for row in board:
        line = "\033[4;30;47m|\033[0m"
        for piece in row:
            if piece == HUMAN:
                line += "\033[4;31;47m\u25CF\033[0m"
            elif piece == AI:
                line += "\033[4;34;47m\u25CF\033[0m"
            else:
                line += "\033[4;30;47m \033[0m"
            line += "\033[4;30;47m|\033[0m"
        print(line)
    print(" 0 1 2 3 4 5 6")
    print("\n")


board = create_board()
place_piece(board, HUMAN, 4)
place_piece(board, AI, 1)
place_piece(board, HUMAN, 1)
place_piece(board, AI, 0)
place_piece(board, HUMAN, 6)
place_piece(board, AI, 3)
place_piece(board, HUMAN, 4)
place_piece(board, AI, 3)
place_piece(board, HUMAN, 4)
place_piece(board, HUMAN, 4)
place_piece(board, HUMAN, 4)
place_piece(board, HUMAN, 4)
os.system('clear')
print("\n Connect Four!\n")
display(board)
