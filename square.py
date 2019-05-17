# Minesweeper square module

# Square char options:  ['-', ' ', 'X', 1-8]
# Square value options: [-1 = mine, 0 = open, 1-8 = mines surrounding]

# Square class definition
class Square:
    # Constructor
    def __init__(self):
        self.char = '-'
        self.value = 0
    # Fill a square with the given value and the appropriate char
    def fillSquare(self, value, flag = False):
        if value == '0':
            self.char = '-'
            self.value = 0
        elif value == '1':
            self.char = ' '
            self.value = 0
        elif value.upper() == value:
            self.char = '-'
            self.value = ord(value) - 64
        else:
            self.char = str(ord(value) - 96)
            self.value = ord(value) - 96
        if flag:
            self.char = '#'
    # Uncover a square and reveal its value
    def uncover(self):
        if self.char == '-':
            if self.value == -1:
                self.char = 'X'
            elif self.value == 0:
                self.char = ' '
            else:
                self.char = str(self.value)
    def isUncovered(self):
        return (self.char != '-' and self.char != '#')
    # Set a flag on a square if it is covered
    def flag(self):
        if self.char == '-':
            self.char = '#'
            return True
        else:
            return False
    # Remove a flag from a square if it is flagged
    def unflag(self):
        if self.char == '#':
            self.char = '-'
            return True
        else:
            return False
