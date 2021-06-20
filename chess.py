from piece import Piece  as P
from board import BoardState as BS

class Game(object):

    @staticmethod
    def generateNewBoard():
        return [[" " for _ in range(8)] for _ in range(8)]
    
    def __init__(self,name1,name2):
        self.p1 = name1
        self.p2 = name2
        self.boardState = BS(generateNewBoard())
        self.moves = 0

        #game states:
        #   0: initial state
        #   1: p1 turn
        #   2: p2 turn
        #   3: p1 win
        #   4: p2 win
        self.gameState = 0

        


