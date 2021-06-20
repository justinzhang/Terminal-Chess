#creates the boardState class,
# includes an

class BoardState(object):
    def __init__(self,board):
        self.board = board
        self.piecesLeft = 0
        self.check = False
    
    def printBoard():
        # first print the column headers
        print("       ", end="")
        for col in range(cols):
            offset = 65 
            print(str(chr(col+offset)).center(3), " ", end="")
        print('\n       ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~')
        # now print the board
        for row in range(rows):
            print(f"    {row+1}|", end="")
            for col in range(cols):
                print(self.board[row][col].center(3), " ", end="")
            print()
        print('\n')

