import os, time
import numpy as np
import random

ROWS = 6
COLUMNS = 7
EMPTY = 0
HUMAN = 1
AI = 2

#farthest space where a winning connection may start
MAX_SPACE_TO_WIN = 3

GAME_WON = False
WINNER = 0

def create_board():
    return np.zeros((ROWS, COLUMNS), np.int8)


#returns false if column is full
def is_valid_column(board, column):
    return board[0][column - 1] == EMPTY


def place_piece(board, player, column):
    if column in range(1, 8):
        index = column - 1
        for row in reversed(range(ROWS)):
            if board[row][index] == EMPTY:
                board[row][index] = player
                return True
    return False


#detects if winning move was done
def detect_win(board, key):
    #horizontal
    for col in range(COLUMNS - MAX_SPACE_TO_WIN):
        for row in range(ROWS):
            if board[row][col] == key and board[row][col+1] == key and board[row][col+2] == key and board[row][col+3] == key:
                return True
    
    #vertical
    for col in range(COLUMNS):
        for row in range(ROWS - MAX_SPACE_TO_WIN):
            if board[row][col] == key and board[row+1][col] == key and board[row+2][col] == key and board[row+3][col] == key:
                return True
    
    #diagonal upwards
    for col in range(COLUMNS - MAX_SPACE_TO_WIN):
        for row in range(ROWS - MAX_SPACE_TO_WIN):
            if board[row][col] == key and board[row+1][col+1] == key and board[row+2][col+2] == key and board[row+3][col+3] == key:
                return True
    
    #diagonal downwards
    for col in range(COLUMNS- MAX_SPACE_TO_WIN):
        for row in range(MAX_SPACE_TO_WIN, ROWS):
            if board[row][col] == key and board[row-1][col+1] == key and board[row-2][col+2] == key and board[row-3][col+3] == key:
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
                line += "\033[4;34;47m\u25CF\033[0m"
            elif piece == AI:
                if col == highlight_index:
                    line = line[:-5] + "\033[4;31;43m|\u25CF|\033[0m"
                    highlight_index = -1
                    continue
                else:
                    line += "\033[4;31;47m\u25CF\033[0m"
            else:
                line += "\033[4;30;47m \033[0m"
            line += "\033[4;30;47m|\033[0m"
        print("                     ║ " + line + " ║")
    print("                     ║  1 2 3 4 5 6 7  ║")
    print("                     ╚═════════════════╝\n")
    print("              Type column to play or 'q' to quit\n")
    print("Next move: ")
    
#prints end message and clears board
def end_game(board):
    os.system("clear")
    print("\nThank you for playing!")
    #exit()
    
    
    
    
#Starter sample
board = create_board()
#place_piece(board, HUMAN, 4)
#place_piece(board, AI, 1)
#place_piece(board, HUMAN, 1)
#place_piece(board, AI, 2)
#place_piece(board, HUMAN, 6)
#place_piece(board, AI, 3)
#place_piece(board, HUMAN, 4)
#place_piece(board, AI, 3)
#place_piece(board, HUMAN, 4)
draw_game(board)

while not GAME_WON:
   
    #Take user input
    pressed_key = input()
    #placeholder AI move. It will change:
    ai_pressed_key = random.randrange(1,8)
    while not is_valid_column(board, ai_pressed_key):
        ai_pressed_key = random.randrange(1,8)

    try:
        pressed_key = int(pressed_key)
    except ValueError:
        pass      
        
    #if valid input
    if pressed_key in range(1,8) and is_valid_column(board,pressed_key):
        #place piece at chosen column
        place_piece(board, HUMAN, pressed_key)
        draw_game(board, pressed_key)
            
        #detect if won
        if detect_win(board, HUMAN):
            WINNER = HUMAN
            GAME_WON = True

        else:    
            #delay
            print("\nWaiting for opponent...")
            time.sleep(1)
            #placeholder AI behavior
            place_piece(board, AI, ai_pressed_key)
            draw_game(board,ai_pressed_key)
            if detect_win(board, AI):
                WINNER = AI
                GAME_WON = True
            
    #if player chooses to quit game
    elif pressed_key == "q":
        end_game(board)
        board = create_board()
            
    #if invalid input
    else:
       print("\nInvalid input, try again...")
       time.sleep(1)
       pressed_key = 0
       draw_game(board, pressed_key)


if WINNER == HUMAN:
    print("Player Won!")
elif WINNER == AI:
    print("AI Won!")
end_game(board)
