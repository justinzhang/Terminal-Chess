#class chessPiece - each chess piece will share
#the board, and the possible moves (generated by specific class)

class Piece(object):
    def __init__(self,row,col,board):
        self.row = row
        self.col = col

        #same board inst
        self.board = board
        self.moves = []

    def printMoves():
        print(self.moves)