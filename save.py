# Minesweeper save module

import os  # Path module
import sys # Path module

# SaveCode derived from Exception class
# SaveCode Errors:
#   0 - No save file found
#   1 - Save file is empty or corrupt
class SaveCode(Exception):
    # Constructor
    def __init__(self, errorCode):
        self.errorCode = errorCode

# Function checkSave(): Checks the validity of the save file
def checkSave():
    # Open file
    try:
        with open(os.path.join((sys.path[0]), "savegame.txt")) as file:
            fileString = file.read()
    except FileNotFoundError:
        raise SaveCode(0)
    # Store info
    try:
        rows = int(fileString[0:2])
        cols = int(fileString[2:4])
        mines = int(fileString[4:7])
        flags = int(fileString[7:10])
    except ValueError:
        raise SaveCode(1)

    # Check 1: Number of flags matches number of '!'s
    if (fileString.count('!') != flags):
        raise SaveCode(1)
    # Check 2: Number of mines matches number of '?'s
    if (fileString.count('?') != mines):
        raise SaveCode(1)
    # Check 3: Size of string matches dimensions
    if ((len(fileString) - 10 - flags) != (rows * cols)):
        raise SaveCode(1)
    # String is valid!
    return

# Function deleteSave(): Deletes the current save file if it exists
def deleteSave():
    try:
        os.remove(os.path.join((sys.path[0]), "savegame.txt"))
    except:
        pass

# Function createSave(): Creates a save file from the given board
def createSave(board):
    # First delete original save file
    deleteSave()
    # Create initial file string to append to
    fileString = ""
    fileString += "{:0>2}".format(str(board.numRows))
    fileString += "{:0>2}".format(str(board.numColumns))
    fileString += "{:0>3}".format(str(board.numMines))
    fileString += "{:0>3}".format(str(board.numFlags))
    # Now output characters
    for row in board.box:
        for square in row:
            if square.char == '#':
                fileString += '!'
            if square.value == 0:
                if square.char == '-':
                    fileString += '0'
                else:
                    fileString += '1'
            else:
                if square.char == '-' or square.char == '#':
                    fileString += chr(square.value + 64)
                else:
                    fileString += chr(square.value + 96)
    # Now write the filestring to a save file
    with open(os.path.join((sys.path[0]), "savegame.txt"), "w+") as file:
        file.write(fileString)
                
