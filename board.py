# Minesweeper board class module

import square # Square class module
import os     # Path module
import sys    # Path module
import menu   # Menu module
import random # Random integer module

# Modify this constant to change max size
MAX_SIZE = 30

# Board class definition
class Board:
    # Constructor
    def __init__(self, rows, columns, mines, flags = 0):
        self.numRows = rows
        self.numColumns = columns
        self.numMines = mines
        self.numFlags = flags
        # Two-dimensional array
        self.box = [[square.Square() for j in range(columns)] for i in range(rows)]
    # Add mines in random positions across the board
    def randomizeMines(self):
        for i in range(self.numMines):
            dupe = True
            while dupe:
                row = random.randint(0, self.numRows - 1)
                column = random.randint(0, self.numColumns - 1)
                if (self.box[row][column]).value != -1:
                    (self.box[row][column]).value = -1
                    dupe = False
    # Return tuples of the surrounding squares by index (row, column)
    def findSurroundingSquares(self, row, column):
        surrounding = [(row - 1, column - 1), (row, column - 1), (row + 1, column - 1),
                       (row - 1, column), (row + 1, column),
                       (row - 1, column + 1), (row, column + 1), (row + 1, column + 1)]
        # Start eliminating squares with -1 or (numRows)
        invalid = []
        for aTuple in surrounding:
            if (aTuple[0] == -1 or aTuple[1] == -1 or
                aTuple[0] == self.numRows or aTuple[1] == self.numColumns):
                invalid.append(aTuple)
        # Now delete all invalid
        for item in invalid:
            surrounding.remove(item)
        return surrounding
    # Find values for squares that touch mines
    def findValues(self):
        i = 0
        for row in self.box:
            j = 0
            for square in row:
                val = 0
                if square.value != -1:
                    squares = self.findSurroundingSquares(i, j)
                    for value in squares:
                        if self.box[value[0]][value[1]].value == -1:
                            val += 1
                    square.value = val
                j += 1
            i += 1
    # Check for whether the game is over (win or lose)
    def gameOver(self):
        # First, check to see if a mine is present on the board
        allCoveredSquaresAreMines = True
        for row in self.box:
            for square in row:
                if square.char == 'X':
                    return 2
                elif square.char == '-':
                    if square.value != -1:
                        allCoveredSquaresAreMines = False
        return allCoveredSquaresAreMines # Implicit type cast
    # Uncover a square
    def uncover(self, theSquare, newSq = False):
        if self.box[theSquare[0]][theSquare[1]].isUncovered() and newSq == True:
            self.specUncover(theSquare)
        else:
            self.box[theSquare[0]][theSquare[1]].uncover()
            if self.box[theSquare[0]][theSquare[1]].value == 0:
                others = self.findSurroundingSquares(theSquare[0], theSquare[1])
                for square in others:
                    if self.box[square[0]][square[1]].char == '-':
                        self.uncover(square)
    # Uncover all surrounding squares of an uncovered square
    # NOTE: This only works if the current square has the
    #       same value as the number of flags touching it
    def specUncover(self, theSquare):
        # Check to make sure it touches the right amount of flags
        flags = 0
        surrounding = self.findSurroundingSquares(theSquare[0], theSquare[1])
        for square in surrounding:
            if self.box[square[0]][square[1]].char == '#':
                flags += 1
        if flags == self.box[theSquare[0]][theSquare[1]].value:
        # Recursive call for each of the surroundng squares
            for square in surrounding:
                self.uncover(square, False)
    # Put a flag over a square
    def flag(self, theSquare):
        if self.box[theSquare[0]][theSquare[1]].char == '#':
            self.unflag(theSquare)
        elif self.box[theSquare[0]][theSquare[1]].flag():
            self.numFlags += 1
    # Remove a flag from a square (if it exists)
    def unflag(self, theSquare):
        if self.box[theSquare[0]][theSquare[1]].unflag():
            self.numFlags -= 1

# Function loadBoard(): Create a board from a save file
def loadBoard():
    with open(os.path.join((sys.path[0]), "savegame.txt")) as file:
        fileString = file.read()
    rows = int(fileString[0:2])
    cols = int(fileString[2:4])
    mines = int(fileString[4:7])
    flags = int(fileString[7:10])
    board = Board(rows, cols, mines, flags)
    fileString = fileString[10:] # Rest of file
    # Now fill the squares
    i = 0
    for row in board.box:
        for square in row:
            if (fileString[i] == '!'):
                square.fillSquare(fileString[i+1], True)
                i += 1
            else:
                square.fillSquare(fileString[i])
            i += 1
    return board

# Function createBoard(): Generate a new board with given specs
def createBoard():
    menu.clearScreen()
    print("Choose game board size:")
    print("(1) Beginner - 9 x 9, 10 mines")
    print("(2) Intermediate - 16 x 16, 40 mines")
    print("(3) Expert - 16 x 30, 99 mines")
    print("(C) Custom size...")
    choice = menu.getChoice(['1', '2', '3', 'C'], 1)
    if choice == '1':
        board = Board(9, 9, 10)
    elif choice == '2':
        board = Board(16, 16, 40)
    elif choice == '3':
        board = Board(16, 30, 99)
    else:
        # Custom dimensions
        rows = menu.getNumInRange(1, MAX_SIZE, "Enter number of rows")
        columns = menu.getNumInRange(1, MAX_SIZE, "Enter number of columns")
        mines = menu.getNumInRange(1, rows * columns, "Enter number of mines")
        board = Board(rows, columns, mines)
    # Now to randomize mines and find values
    board.randomizeMines()
    board.findValues()
    print("Loaded.")
    return board

# Function printBoard: Prints the given board to the screen
def printBoard(theBoard):
    menu.clearScreen()
    # First, print column headers
    print("   ", end="") # Offset
    for col in range(theBoard.numColumns):
        print(chr(col+65), end=" ")
    # Now print the rest of the board with row headers
    print(end='\n')
    for row in theBoard.box:
        printString = chr(theBoard.box.index(row)+65) + " |"
        for square in row:
            printString += "{}|".format(square.char)
        print(printString)
    # Mine count
    print("\n" + "Mines: " + str(theBoard.numMines - theBoard.numFlags) + "\n")
