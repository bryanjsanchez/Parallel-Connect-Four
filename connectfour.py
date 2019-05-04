import os, time
import numpy as np
import random


ROWS = 6
COLUMNS = 7
EMPTY = 0
HUMAN = 1
AI = 2

MAX_SPACE_TO_WIN = 3 # Farthest space where a winning connection may start

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

def clone_and_place_piece(board, player, column):
    new_board = board.copy()
    place_piece(new_board, player, column)
    return new_board


def detect_win(board, player):
    # Horizontal win
    for col in range(COLUMNS - MAX_SPACE_TO_WIN):
        for row in range(ROWS):
            if board[row][col] == player and board[row][col+1] == player and \
                    board[row][col+2] == player and board[row][col+3] == player:
                return True
    # Vertical win
    for col in range(COLUMNS):
        for row in range(ROWS - MAX_SPACE_TO_WIN):
            if board[row][col] == player and board[row+1][col] == player and \
                    board[row+2][col] == player and board[row+3][col] == player:
                return True
    # Diagonal upwards win
    for col in range(COLUMNS - MAX_SPACE_TO_WIN):
        for row in range(ROWS - MAX_SPACE_TO_WIN):
            if board[row][col] == player and board[row+1][col+1] == player and \
                    board[row+2][col+2] == player and board[row+3][col+3] == player:
                return True
    # Diagonal downwards win
    for col in range(COLUMNS - MAX_SPACE_TO_WIN):
        for row in range(MAX_SPACE_TO_WIN, ROWS):
            if board[row][col] == player and board[row-1][col+1] == player and \
                    board[row-2][col+2] == player and board[row-3][col+3] == player:
                return True
    return False
    

def score(board, player):
    score = 0
    # Horizontal pieces
    for col in range(COLUMNS - MAX_SPACE_TO_WIN):
        for row in range(ROWS):
            adjacent_pieces = board[row][col:col+4]
            score += evaluate_adjacents(adjacent_pieces, player)
    # Vertical pieces
    for col in range(COLUMNS):
        for row in range(ROWS - MAX_SPACE_TO_WIN):
            adjacent_pieces = [board[row][col], board[row+1][col], 
                                board[row+2][col], board[row+3][col]] 
            score += evaluate_adjacents(adjacent_pieces, player)
    # Diagonal upwards pieces
    for col in range(COLUMNS - MAX_SPACE_TO_WIN):
        for row in range(ROWS - MAX_SPACE_TO_WIN):
            adjacent_pieces = [board[row][col], board[row+1][col+1], 
                                board[row+2][col+2], board[row+3][col+3]] 
            score += evaluate_adjacents(adjacent_pieces, player)
    # Diagonal downwards pieces
    for col in range(COLUMNS - MAX_SPACE_TO_WIN):
        for row in range(MAX_SPACE_TO_WIN, ROWS):
            adjacent_pieces = [board[row][col], board[row-1][col+1], 
                    board[row-2][col+2], board[row-3][col+3]]
            score += evaluate_adjacents(adjacent_pieces, player)
    return score

def evaluate_adjacents(adjacent_pieces, player):
    score = 0
    opponent = AI
    if player == AI:
        opponent = HUMAN
    if np.count_nonzero(adjacent_pieces == player) == 4:
        score += 999
    if np.count_nonzero(adjacent_pieces == player) == 3 and \
        np.count_nonzero(adjacent_pieces == EMPTY) == 1:
        score += 50  
    if np.count_nonzero(adjacent_pieces == player) == 2 and \
        np.count_nonzero(adjacent_pieces == EMPTY) == 2:
        score += 10
    return score

def draw_game(board, turn, game_over=False, AI_move=0):
    highlight_index = AI_move - 1
    print( "\033c") # Clear screen
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
            print( "\033c") # Clear screen
            print("\nThank you for playing!")
            exit()
        # Invalid input
        else:
           print("\nInvalid input, try again...")
           time.sleep(2)
           draw_game(board, turn, AI_move = AI_move)

    elif turn == AI:
        # Placeholder AI move. It will change:
        best_move = -1
        best_score = 0
        for col in range(1,8):
            current_score = score(clone_and_place_piece(board, AI, col), AI)
            if current_score > best_score:
                best_move = col
                best_score = current_score
        if best_move in range(1,8):
            AI_move = best_move
        else:
            AI_move = random.randrange(1,8)
            while not is_valid_column(board, AI_move):
                AI_move = random.randrange(1,8)
            # time.sleep(2)
        place_piece(board, AI, AI_move)
        is_game_won = detect_win(board, AI)
        if is_game_won:
            draw_game(board, turn, game_over=True, AI_move=AI_move)
            break
        else:
            turn = HUMAN
            draw_game(board, turn, AI_move=AI_move)
            continue
print("                   Thank you for playing!")
exit()
