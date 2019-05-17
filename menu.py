# Minesweeper menu module (for various UI interactions and functions)

# Function clearScreen(): Clears the console screen.
def clearScreen():
    import os # Used for cls
    # Windows: 'cls'
    # POSIX: 'clear'
    os.system('cls' if os.name == 'nt' else 'clear')

# Function getChar(): Gets a character without pressing enter.
def getChar(numBytes, listOfOneChars):
    import sys # Flush output
    sys.stdout.flush() # Important for executing prior print statement
    # Check for Windows system
    try:
        import msvcrt
        answer = ""
        for i in range(numBytes):
            ch = msvcrt.getche().decode()
            ch = ch.upper()
            if (ch in listOfOneChars):
                print('')
                return ch
            answer += ch
        print('') # Starts a new line following function call
        return answer
    # Else, POSIX system
    except ImportError:
        import tty, sys, termios
        fd = sys.stdin.fileno() # File descriptor
        oldSettings = termios.tcgetattr(fd) # tty attributes for fd
        try:
            answer = ""
            tty.setraw(fd) # Change mode to raw
            for i in range(numBytes):
                ch = sys.stdin.read(1) # Read in byte(s)
                print(ch, end='') # Puts the character to the console
                ch = ch.upper() # Make uppercase
                sys.stdout.flush()
                if (ch in listOfOneChars):
                    termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)
                    print('')
                    return ch
                answer += ch
        finally: # Change after discarding queued input
            termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)
        print('')
        return answer

# Function getSeed: Used to get an integer seed at startup.
def getSeed():
    print("Enter seed for the random value generator:")
    try:
        seed = int(input(" >> "))
        return seed
    except ValueError:
        return None

# Function beginMessage: Displayed at startup.
def beginMessage():
    clearScreen()
    print("*" * 24)
    print("{:<23}".format("*  Minesweeper v. 1.0") + "*")
    print("{:<23}".format("*  By Trevor Natiuk") + "*")
    print("*" * 24)
    print("\n")
    
# Function wait: Wait for key to be pressed.
# 0 = begin
# 1 = continue
# 2 = exit
def wait(num):
    word = ["begin", "continue", "exit"]
    print("Press any key to {}... ".format(word[num]), end='')
    getChar(1, ['All'])

# Function yesNo: Get yes or no from user.
def yesNo():
    accepted = ['Y', 'N']
    char = 'n'
    while char == 'n':
        print("(y/n) >> ", end='')
        char = getChar(1, accepted)
        if char in accepted:
            return (char == 'Y')

# Function getChoice: Get a choice out of a set of accepted values
def getChoice(accepted, numChars):
    raw = 'x'
    while raw == 'x':
        print(" >> ", end='')
        raw = getChar(numChars, accepted)
        if raw[0] not in accepted:
            if numChars != 1:
                # Assume you're now trying for a square
                return raw
            else:
                raw = 'x'
        else:
            return raw

# Function getNumberInRange: Get a number in a specified range
def getNumInRange(left, right, message):
    print(message)
    while True:
        num = input("({}-{}) >> ".format(left, right))
        if num == "":
            num = 'x'
        try:
            num = int(num)
            if (num >= left and num <= right):
                return num
            else:
                continue
        except ValueError:
            continue

# Function mainMenu: Main prompt for Minesweeper options
def mainMenu():
    print("Enter square: [row][column] OR:" + '\n' +
          "(1) - Flag/unflag a square" + '\n' +
          "(2) - Click the face" + '\n' +
          "(3) - Exit Minesweeper")
    choice = getChoice(['1', '2', '3'], 2)
    return choice

# Function gameOverMenu: Main prompt for game over options
def gameOverMenu(string):
    print("You {}!".format(string) + '\n' + '\n' +
          "(2) - Click the face" + '\n' +
          "(3) - Exit Minesweeper")
    choice = getChoice(['2', '3'], 1)
    return choice

# Function getSquare: Returns a tuple of a square in the board
def getSquare(rows, columns):
    square = "00"
    while square == "00":
        print(" >> ", end='')
        square = getChar(2, ['None'])
        row = square[0].upper()
        col = square[1].upper()
        if ord(row) < 65 or ord(row) > 64 + rows:
            square = "00"
        if ord(col) < 65 or ord(col) > 64 + columns:
            square = "00"
        else:
            return (ord(row) - 65, ord(col) - 65)
