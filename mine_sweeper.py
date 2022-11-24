import random
import sys

BOARD_SIZE = 0
GAME_BOARD = []
NUMBER_OF_MINES = 0
SYMBOL_FLAG = "⚑"
SYMBOL_PEACE = "❀"
SYMBOL_MINE = "☢"
SYMBOL_UNKNOWN = "-"
SYMBOL_CLEAR = " "

class Square:
    def __init__(self, row, column) -> None:
        self.status = SYMBOL_UNKNOWN
        self.row = row
        self.column = column
        self.mine = False
        self.neighbours = []
        self.danger = 0
        self.cleared = False

def display():
    for x in range(BOARD_SIZE):
        # First line logic.
        if x == 0:
            # Initial number spacing.
            print(" ", end="")
            for i in range(BOARD_SIZE):
                # Spacing between numbers
                print("   " + str(i+1), end="")
            # Completing the first row since x is still 0.
            print("\n  ╔═" + ("══╦═" * (BOARD_SIZE - 1)) + "══╗")
            print("1 ║", end="")
            for y in range(BOARD_SIZE):
                print(" " + str(GAME_BOARD[x][y].status) + " ║", end="")
            print("\n  ╠═" + ("══╬═" * (BOARD_SIZE - 1)) + "══╣")

        # Last line logic. Also remove the extra space if the board size is 10.
        elif x == BOARD_SIZE-1:
            if BOARD_SIZE == 10:
                print(str(BOARD_SIZE) + "║", end="")
            else:
                print(str(BOARD_SIZE) + " ║", end="")
            for y in range(BOARD_SIZE):
                print(" " + str(GAME_BOARD[x][y].status) + " ║", end="")
            print("\n  ╚═" + "══╩═" * (BOARD_SIZE - 1) + "══╝")
        
        # Logic for every other line.
        else:
            print(str(x+1) + " ║", end="")
            for y in range(BOARD_SIZE):
                print(" " + str(GAME_BOARD[x][y].status) + " ║", end="")
            print("\n  ╠═" + ("══╬═" * (BOARD_SIZE - 1)) + "══╣")

def startup():
    # Set game parameters.
    global BOARD_SIZE
    global NUMBER_OF_MINES
    global GAME_BOARD
    print("Welcome to Minesweeper! \nTo win, you must clear all squares that don't contain a bomb.\n")
    while True:
        try:
            BOARD_SIZE = int(input("What size board do you want, between 3 and 10 (inclusive)? -> "))
        except ValueError:
            print("Invalid entry. Try again!")
            continue
        if BOARD_SIZE not in range(3, 11):
            print("Invalid range. Try again!")
            continue
        else:
            while True:
                try:
                    NUMBER_OF_MINES = int(input("How many mines do you want? -> "))
                except ValueError:
                    print("Invalid entry. Try again!")
                if NUMBER_OF_MINES >= BOARD_SIZE**2:
                    print("Woah, that's too many. Try again.")
                    continue
                elif NUMBER_OF_MINES == 0:
                    print("I'm sure you can manage with at least 1 mine!")
                else:
                    break

            # Initialise an empty board.
            GAME_BOARD = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

            # Fill that board with Square objects.
            for row in range(BOARD_SIZE):
                for column in range(BOARD_SIZE):
                    GAME_BOARD[row][column] = Square(row, column)

            # link each square to it's neighbours
            for a in range(BOARD_SIZE):
                for b in range(BOARD_SIZE):
                    square = GAME_BOARD[a][b]
                    if a == 0:
                        square.neighbours.append(GAME_BOARD[a+1][b])
                        if b != BOARD_SIZE-1:
                            square.neighbours.append(GAME_BOARD[a + 1][b + 1])
                            square.neighbours.append(GAME_BOARD[a][b+1])
                        if b != 0:
                            square.neighbours.append(GAME_BOARD[a][b-1])
                            square.neighbours.append(GAME_BOARD[a+1][b-1])
                    elif a == BOARD_SIZE-1:
                        square.neighbours.append(GAME_BOARD[a-1][b])
                        if b != BOARD_SIZE-1:
                            square.neighbours.append(GAME_BOARD[a][b+1])
                            square.neighbours.append(GAME_BOARD[a-1][b+1])
                        if b != 0:
                            square.neighbours.append(GAME_BOARD[a-1][b-1])
                            square.neighbours.append(GAME_BOARD[a][b-1])
                    else:
                        square.neighbours.append(GAME_BOARD[a+1][b])
                        square.neighbours.append(GAME_BOARD[a-1][b])
                        if b != BOARD_SIZE-1:
                            square.neighbours.append(GAME_BOARD[a-1][b+1])
                            square.neighbours.append(GAME_BOARD[a][b+1])
                            square.neighbours.append(GAME_BOARD[a+1][b+1])
                        if b != 0:
                            square.neighbours.append(GAME_BOARD[a-1][b-1])
                            square.neighbours.append(GAME_BOARD[a][b-1])
                            square.neighbours.append(GAME_BOARD[a+1][b-1])
            print()
            display()
            print()
            first_move()
            print()
            display()
            print("\nType 'help' for a list of command descriptions.", end="")
            break       

def first_move():
    # Establishes mine locations, ignoring starting dig.
    print("Where would you like to start?")
    while True:
        try:
            a, b = input("Enter an x,y coordinate, comma separated, to dig the first square: -> ").split(',')
        except ValueError:
            print("Invalid entry. Try again!")
            continue
        x = int(b)-1
        y = int(a)-1
        if x >= BOARD_SIZE or y >= BOARD_SIZE:
            print("Out of bounds, try again.")
            continue
        else:
            for _ in range(NUMBER_OF_MINES):
                place_mines(x, y)
            welfare(GAME_BOARD[x][y])
            break

def place_mines(first_row, first_column):
    # Recursively places mines, ignoring starting square and squares with existing mines
    global GAME_BOARD
    x = random.randint(0, BOARD_SIZE-1)
    y = random.randint(0, BOARD_SIZE-1)
    if x == first_row and y == first_column:
        place_mines(first_row, first_column)
    else:
        if not GAME_BOARD[x][y].mine:
            if GAME_BOARD[first_row][first_column] in GAME_BOARD[x][y].neighbours:
                place_mines(first_row, first_column)
            else:
                GAME_BOARD[x][y].mine = True
                for square in GAME_BOARD[x][y].neighbours:
                    square.danger += 1
        else:
            place_mines(first_row, first_column)

def next_turn():
    # Keeps prompting to dig, flag, or end the game
    move = input("\nWould you like to 'dig', 'flag', 'remove' or 'quit'? -> ").lower()
    if move == "quit":
        print("Thanks for playing!")
        # Exit using garbage collection.
        sys.exit()
    elif move == "dig":
        dig()
        print()
        display()
    elif move == "flag":
        flag()
        print()
        display()
    elif move == "remove":
        unflag()
        print()
        display()
    elif move == "help":
        print()
        print("The commands are as follows:")
        print("-------------------------------------------------------------------------")
        print("Type 'quit' to end the game.")
        print("Type 'dig' to uncover a square.")
        print("Type 'flag' to plant a flag and mark it as containing a mine.")
        print("Type 'remove' to removed a placed flag.")
        print("**NOTE** - All coordinates must be comma separated, with no spaces.")
        print("Type 'help' to see these list of commands again.")
        print("-------------------------------------------------------------------------")

    else:
        print("I don't understand. Type 'help' for a list of commands.")

def flag():
    # Flag a square to indicate a potential mine
    while True:
        try:
            a, b = input("Supply an x,y coordinate to flag: -> ").split(',')
        except ValueError:
            print("Invalid entry. Try again!")
            continue
        x = int(b)-1
        y = int(a)-1
        if x >= BOARD_SIZE or y >= BOARD_SIZE:
            print("Out of bounds, try again.")
            continue
        else:
            global GAME_BOARD
            GAME_BOARD[x][y].status = SYMBOL_FLAG
            break

def unflag():
    # Unflags a prevously flagged square.
    while True:
        try:
            a, b = input("Supply an x,y coordinate to unflag: -> ").split(',')
        except ValueError:
            print("Invalid entry. Try again!")
            continue
        x = int(b)-1
        y = int(a)-1
        if x >= BOARD_SIZE or y >= BOARD_SIZE:
            print("Out of bounds, try again.")
            continue
        else:
            global GAME_BOARD
            if GAME_BOARD[x][y].status == SYMBOL_FLAG:
                GAME_BOARD[x][y].status = SYMBOL_UNKNOWN
            else:
                print("\nThere was no flag there.")
            break

def dig():
    # Uncover a square - if it's a bomb, it ends the game. Otherwise reveals nearby empty squares
    while True:
        try:
            a, b = input("Supply an x,y coordinate to dig: ").split(',')
        except ValueError:
            print("Invalid entry. Try again!")
            continue
        x = int(b)-1
        y = int(a)-1
        if x >= BOARD_SIZE or y >= BOARD_SIZE:
            print("Out of bounds, try again.")
            continue
        else:
            if GAME_BOARD[x][y].mine is True:
                print("\nYou have died! Better luck next time.")
                for x in range(BOARD_SIZE):
                    for y in range(BOARD_SIZE):
                        square = GAME_BOARD[x][y]
                        if square.mine is True:
                            square.status = SYMBOL_MINE
                display()
                sys.exit()
            else:
                GAME_BOARD[x][y].status = SYMBOL_CLEAR
                GAME_BOARD[x][y].cleared = True
                welfare(GAME_BOARD[x][y])
                break

def welfare(square, history = []):
    if square.danger == 0:
        square.status = SYMBOL_CLEAR
        square.cleared = True
        for box in square.neighbours:
            if box not in history:
                history.append(box)
                welfare(box, history)
    else:
        if not square.mine:
            square.status = str(square.danger)
            square.cleared = True

def win_state():
    global GAME_BOARD
    uncleared_squares = 0
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            square = GAME_BOARD[x][y]
            if square.cleared == False:
                uncleared_squares += 1
    if uncleared_squares == NUMBER_OF_MINES:
        print("\n\nCongratulations! \nYou found all the mines and didn't die.\n")
        for x in range(BOARD_SIZE):
            for y in range(BOARD_SIZE):
                square = GAME_BOARD[x][y]
                if square.mine:
                    square.status = SYMBOL_PEACE
        display()
        sys.exit()

startup()
while True:
    next_turn()
    win_state()