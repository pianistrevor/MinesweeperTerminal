# Minesweeper 1.0 by Trevor Natiuk
# Written in Python 3.7.3

import menu # Menus and key function
import save  # Save file functions and error code class
import board # Minesweeper board class module
import random # Random integer module

# Get seed
random.seed(menu.getSeed())

# Display welcome message
menu.beginMessage()

#######################
# Check for save file #
#######################

try:
    save.checkSave()
    print("Save file found. Load file?")
    if menu.yesNo():
        gameBoard = board.loadBoard()
        print("Loaded.")
    else:
        gameBoard = board.createBoard()
except save.SaveCode as e:
    if e.errorCode == 0:
        print("No save file found.")
    else:
        print("Save file is either empty or corrupt.")
    menu.wait(0)
    gameBoard = board.createBoard()

menu.wait(1)

########################
# Here begins the game #
########################

userExit = False

# Main loop
while not userExit:
    board.printBoard(gameBoard)
    if gameBoard.gameOver() == 2:
        save.deleteSave()
        choice = menu.gameOverMenu("lose")
    elif gameBoard.gameOver() == 1:
        save.deleteSave()
        choice = menu.gameOverMenu("win")
    else:
        choice = menu.mainMenu()
    if choice == '1':
        gameBoard.flag(menu.getSquare(gameBoard.numRows, gameBoard.numColumns))
    elif choice == '2':
        print("NOTE: If you have a save file, this will NOT" + '\n' +
              "overwrite it. Your current game will be erased" + '\n' +
              "and you will begin a new one from scratch." + '\n' + '\n' +
              "Are you sure you want to restart?")
        if menu.yesNo():
            gameBoard = board.createBoard()
            menu.wait(1)
        continue
    elif choice == '3':
        print("Are you sure you want to exit?")
        if menu.yesNo():
            userExit = True
    else:
        row = choice[0].upper()
        col = choice[1].upper()
        if ord(row) < 65 or ord(row) > 64 + gameBoard.numRows:
            continue
        if ord(col) < 65 or ord(col) > 64 + gameBoard.numColumns:
            continue
        else:
            gameBoard.uncover((ord(row) - 65, ord(col) - 65), True)

# End of game; will we save?
if (gameBoard.gameOver() == 0):
    print("NOTE: This will delete other save data." + '\n' +
          "Would you like to save your game?")
    if (menu.yesNo()):
        save.createSave(gameBoard)

# End of program

