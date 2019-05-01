import os, time
import numpy as np
import random


ROWS = 6
COLUMNS = 7
EMPTY = 0
HUMAN = 1
AI = 2


def create_board():
    return np.zeros((ROWS, COLUMNS), np.int8)


def is_valid_column(board, column):
    return board[0][column - 1] == EMPTY


def place_piece(board, player, column):
    index = column - 1
    for row in reversed(range(ROWS)):
        if board[row][index] == EMPTY:
            board[row][index] = player
            return


def detect_win(board, key):
    MAX_SPACE_TO_WIN = 3 # Farthest space where a winning connection may start
    # Horizontal win
    for col in range(COLUMNS - MAX_SPACE_TO_WIN):
        for row in range(ROWS):
            if board[row][col] == key and board[row][col+1] == key and \
                    board[row][col+2] == key and board[row][col+3] == key:
                return True
    # Vertical win
    for col in range(COLUMNS):
        for row in range(ROWS - MAX_SPACE_TO_WIN):
            if board[row][col] == key and board[row+1][col] == key and \
                    board[row+2][col] == key and board[row+3][col] == key:
                return True
    # Diagonal upwards win
    for col in range(COLUMNS - MAX_SPACE_TO_WIN):
        for row in range(ROWS - MAX_SPACE_TO_WIN):
            if board[row][col] == key and board[row+1][col+1] == key and \
                    board[row+2][col+2] == key and board[row+3][col+3] == key:
                return True
    # Diagonal downwards win
    for col in range(COLUMNS - MAX_SPACE_TO_WIN):
        for row in range(MAX_SPACE_TO_WIN, ROWS):
            if board[row][col] == key and board[row-1][col+1] == key and \
                    board[row-2][col+2] == key and board[row-3][col+3] == key:
                return True
    return False
    

def draw_game(board, turn, game_over=False, AI_move=0):
    highlight_index = AI_move - 1
    os.system('clear')
    print("  ____                            _     _____                ")
    print(" / ___|___  _ __  _ __   ___  ___| |_  |  ___|__  _   _ _ __ ")
    print("| |   / _ \| '_ \| '_ \ / _ \/ __| __| | |_ / _ \| | | | '__|")
    print("| |__| (_) | | | | | | |  __/ (__| |_  |  _| (_) | |_| | |   ")
    print(" \____\___/|_| |_|_| |_|\___|\___|\__| |_|  \___/ \__,_|_|\n")
    print("                     ╔═════════════════╗")
    if turn == HUMAN and not game_over:
        print("                     ║   Your turn!    ║")
    elif turn == AI and not game_over:
        print("                     ║ Computer's turn ║")
    elif turn == HUMAN and game_over:
        print("                     ║    You win!!    ║")
    elif turn == AI and game_over:
        print("                     ║  Computer wins  ║")
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
    if not game_over:
        print("              Type column to play or 'q' to quit\n")
        if turn == HUMAN:
            print("Your move: ")
        else:
            print("Waiting for computer...")
    

# Starter sample
board = create_board()
turn = HUMAN
draw_game(board, turn)
is_game_won = False
AI_move = -1
while not is_game_won:
    
    if turn == HUMAN:
        # Take user input
        pressed_key = input()
        try:
            pressed_key = int(pressed_key)
        except ValueError:
            pass      
        
        # If typed 1 to 7
        if pressed_key in range(1,8) and is_valid_column(board, pressed_key):
            place_piece(board, HUMAN, pressed_key)
            is_game_won = detect_win(board, turn)
            print(detect_win(board, turn))
            if is_game_won:
                draw_game(board, turn, game_over=True)
                break
            else:
                turn = AI
                draw_game(board, turn)
                continue
        # If player chooses to quit game
        elif pressed_key == "q":
            os.system("clear")
            print("\nThank you for playing!")
            exit()
        # Invalid input
        else:
           print("\nInvalid input, try again...")
           time.sleep(2)
           draw_game(board, turn, AI_move = AI_move)

    elif turn == AI:
        # Placeholder AI move. It will change:
        AI_move = random.randrange(1,8)
        while not is_valid_column(board, AI_move):
            AI_move = random.randrange(1,8)
        time.sleep(2)
        place_piece(board, AI, AI_move)
        is_game_won = detect_win(board, AI)
        if is_game_won:
            draw_game_(board, turn, game_over=True, AI_move=AI_move)
            break
        else:
            turn = HUMAN
            draw_game(board, turn, AI_move=AI_move)
            continue
print("                   Thank you for playing!")
exit()
