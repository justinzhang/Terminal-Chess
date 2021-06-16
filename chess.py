#################################################
#Justin Zhang - Chess implementation
#todo: clean up file
#################################################

import math, copy

#################################################
# Helper functions
#################################################

def almostEqual(d1, d2, epsilon=10**-7):
    # note: use math.isclose() outside 15-112 with Python version 3.5 or later
    return (abs(d2 - d1) < epsilon)

import decimal
def roundHalfUp(d):
    # Round to nearest with ties going away from zero.
    rounding = decimal.ROUND_HALF_UP
    # See other rounding options here:
    # https://docs.python.org/3/library/decimal.html#rounding-modes
    return int(decimal.Decimal(d).to_integral_value(rounding=rounding))


#~~~~~~~~~~~~~~~~~~playSimpleChess()~~~~~~~~~~~~~~~~
#imported from an old 112 hw assignment

#The following function is from:
#https://www.cs.cmu.edu/~112/notes/notes-2d-lists.html 

def make2dList(entry,rows,cols):
    return [ ([entry] * cols) for row in range(rows) ]

def makeChessBoard():
    chessBoard = make2dList('[ ]',7,8)
    pieces1=['R','KN','B','Q','KI','B','KN','R','P','P','P','P','P','P','P','P']
    pieces2=['r','kn','b','q','ki','b','kn','r','p','p','p','p','p','p','p','p']
    rows = len(chessBoard)
    cols = len(chessBoard[0])
    chessBoard = [pieces1[:cols] , pieces1[cols:]] + chessBoard[2:5]
    chessBoard += [pieces2[cols:] , pieces2[:cols]]
    return chessBoard

#prints a new chessboard by default, used to update board in console
def printChessBoard(board=makeChessBoard()):
    rows = len(board)
    cols = len(board[0])
    print()
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
            print(board[row][col].center(3), " ", end="")
        print()
    print('\n')

#translates number coordinates back into a chess coordinate string
def chessCoord(row,col):
    offset = 65
    stringRow = str(row+1)
    stringCol = chr(col + offset)
    return stringCol + stringRow

#takes a chess coord string and returns number coordinates
def numCoord(chessString):
    rowCor,colCor = None,None
    offset = 65
    singleDigitFlag = False

    for char in chessString:
        if char.isdigit():
            rowCor = int(char) - 1
            #multiple digit coordinates not allowed
            singleDigitFlag = not singleDigitFlag
            if not singleDigitFlag:
                print("No such coordinate!", end = " ")
                return None
        if char.isalpha():
            colCor = ord(char.upper()) - offset
    if rowCor == None or colCor == None or rowCor > 6 or colCor > 7:
        print("No such coordinate!", end = " ")
        return None
    return rowCor,colCor


#returns the coordinates, from 0, and the piece. If no piece, returns none
#used when moving a piece/telling if a location is valid for movement
def pieceInfo(board,position,p1Flag):
    if numCoord(position) == None:
        return None
    rowCor,colCor = numCoord(position)
    if board[rowCor][colCor] == '[ ]':
        print("No piece here!", end = " ")
        return None
    piece = board[rowCor][colCor]
    if p1Flag and piece.isupper():
        print("Not your piece! You are lowercase!", end = " ")
        return None

    if not p1Flag and piece.islower():
        print("Not your piece! You are upper!", end = " ")
        return None
    
    return rowCor, colCor, piece

#takes in a potential space and if it is empty, then movement is legal
def legalMove(row,col,board):
    potentialSpace = board[row][col]
    return potentialSpace == '[ ]'

def legalEat(row,col,board,p1Flag):
    potEat = board[row][col]
    eatFlag = (p1Flag and potEat.isupper()) or (not p1Flag and potEat.islower())
    #Lowercase can only eat upercase and vice versa!
    if eatFlag:
        return potEat != '[ ]'
    return False

#for conditions that require legalEat or legalMove
def canMove(row,col,board,p1Flag):
    return legalMove(row,col,board) or legalEat(row,col,board,p1Flag)

#checks whether a piece can be upgraded and upgrades it
def upgrade(board,pRow,pCol,p1Flag):
    rows = len(board)
    cols = len(board[0])
    board,pieces1,pieces2,dead1,dead2, = update(board)
    piece = board[pRow][pCol]
    pUpgrades = ['b','q','kn','r']
    upgradeList = list()
    canUpgrade = False
    targetDead = dead1 if p1Flag else dead2
    p1Move = -1 if p1Flag else 1
    
    for dead in targetDead:
        if dead.lower() in pUpgrades:
            canUpgrade = True
            upgradeList.append(dead)
    
    if not canUpgrade:
        print("You cannot go further :(")
        return None
    
    p1Move = -1 if p1Flag else 1
    while canUpgrade:
        which = input(f'Upgrade pawn to one of the following : {upgradeList} ')
        if which in upgradeList:
            move = input(f'Where would you like to move? ')
            while numCoord(move) == None:
                print("Not a coordinate! Try again!", end = " ")
                move = input(f'Where would you like to move? ')
            move = numCoord(move)
            moveRow,moveCol = move[0],move[1]
            #rangeFlag checks if the move is possible
            rangeFlag = (moveRow == pRow + p1Move) and abs(moveCol - pCol) <= 1 
            
            if canMove(moveRow,moveCol,board,p1Flag) and rangeFlag:
                board[pRow][pCol] = '[ ]'
                board[moveRow][moveCol] = which
                canUpgrade = not canUpgrade
            else:
                print("Not possible! Try again!", end = " ")
        else:
            print(f"Unknown piece! Try again!", end = " ")
    printChessBoard(board)
    return board


#Runs through the new board state and returns lists of pieces alive and dead
def update(board):
    rows = len(board)
    cols = len(board[0])
    
    dead1=['r','kn','b','q','ki','b','kn','r','p','p','p','p','p','p','p','p']
    dead2=['R','KN','B','Q','KI','B','KN','R','P','P','P','P','P','P','P','P']
    
    pieces1,pieces2 = list(),list()
    for row in range(rows):
        for col in range(cols):
            piece = board[row][col]
            if piece.islower():
                dead1.remove(piece)
                pieces1.append(piece)
            elif piece.isupper():
                dead2.remove(piece)
                pieces2.append(piece)
    
    return board,sorted(pieces1),sorted(pieces2),dead1,dead2

#finds what piece is chosen and runs the correct piece function
def whatPiece(board,position,p1Flag):
    row,col,piece = pieceInfo(board,position,p1Flag)
    if piece.lower() == 'p':
        return pawn(board,position,p1Flag)
    if piece.lower() == 'r':
        return rook(board,position,p1Flag)
    if piece.lower() == 'kn':
        return knight(board,position,p1Flag)
    if piece.lower() == 'b':
        return bishop(board,position,p1Flag)
    if piece.lower() == 'q':
        return queen(board,position,p1Flag)
    if piece.lower() == 'ki':
        return king(board,position,p1Flag)
    

#a general move function for all pieces
def movePiece(board,row,col,piece,moves):
    rows = len(board)
    cols = len(board[0])
    if moves == []:
        print("Impossible to move this piece currently. Choose another!"
        ,end = " ")
        return None

    userMove = None
    printChessBoard(board)

    while userMove not in moves:
        chessMove = input(f"move {chessCoord(row,col)} where?: ")
        userMove = numCoord(chessMove)
        if userMove not in moves:
            print("Not possible!")
            return None

    board[row][col] = '[ ]'
    board[userMove[0]][userMove[1]] = piece
    printChessBoard(board)

    return board

#This is the function for moving a pawn
#If [b,kn,q,r] is in dead, then pawn can enter last row to upgrade. Else cannot
def pawn(board,position,p1Flag):
    rows,cols = len(board),len(board[0])
    row,col,piece = pieceInfo(board,position,p1Flag)
    moveUp = row -1 if piece.islower() else row + 1
    #inspired by word search
    colMoves = [-1,1]
    moves = list()
    
    #check if pawn is about to upgrade ie reach the end of the board
    if (row == 1 and p1Flag) or (row == (rows -1) - 1 and not p1Flag):
        return upgrade(board,row,col,p1Flag)
        #if no upgrade, then board stays the same

    elif row != rows or row != 0:
        for colMove in colMoves:
            eatMove = col + colMove
            #this is for eating other pieces
            if 0 <= eatMove < cols and legalEat(moveUp,eatMove,board,p1Flag):
                moves.append((moveUp,eatMove))
            #and this is for normal movement
        if legalMove(moveUp,col,board):
            moves.append((moveUp,col))
    #we now have a list of all posible moves!

    return movePiece(board,row,col,piece,moves)

#helper function for rook. Rook needs to check for consecutive line spaces
def rookMoves(board,line,direction,pieceRow,pieceCol,p1Flag):
    rows,cols = len(board),len(board[0])
    rowFlag = line == 'row'
    changing = pieceCol if rowFlag else pieceRow
    static = pieceRow if rowFlag else pieceCol
    lenLine = cols if rowFlag else rows
    index = changing + direction
    consecFlag = True
    moves = list()
    while (0 <= index < lenLine) and consecFlag:
        currSpace = board[static][index] if rowFlag else board[index][static]
        if currSpace == '[ ]':
            possCoord = (static,index) if rowFlag else (index,static)
            moves.append(possCoord)
            index += direction
        else: 
            
            possCoord = (static,index) if rowFlag else (index,static)
            
            if legalEat(possCoord[0],possCoord[1],board,p1Flag):
                moves.append(possCoord)
            consecFlag = not consecFlag
    return moves

#rooks can move in straight lines in any direction
def rook(board,position,p1Flag):
    rows,cols = len(board),len(board[0])
    pieceRow,pieceCol,piece = pieceInfo(board,position,p1Flag)
    currRow = board[pieceRow]
    currCol = list()
    for row in range(rows):
        currCol.append(board[row][pieceCol])
    
    moves = list()
    directions = [-1,1]
    lines = ['row','col']

    for line in lines:
        for direction in directions:
            moves += rookMoves(board,line,direction,pieceRow,pieceCol,p1Flag)
    #we now have all our possible moves!

    return movePiece(board,pieceRow,pieceCol,piece,moves)

#A bishop can move in any diagonal. Stops when reaches a piece
#functionally similar to rook, except both row and col increase simultaniously
def bishopMoves(board,pieceRow,pieceCol,rowDir,colDir,p1Flag):
    rows,cols = len(board),len(board[0])
    lenLine = rows if rows<cols else cols
    rIndex = pieceRow + rowDir
    cIndex = pieceCol + colDir
    consecFlag = True
    moves = list()
    while (0 <= rIndex < rows) and (0 <= cIndex < cols) and consecFlag:
        currSpace = board[rIndex][cIndex]
        possCoord = (rIndex,cIndex)
        if currSpace == '[ ]':
            moves.append(possCoord)
            rIndex += rowDir
            cIndex += colDir
        else:
            if legalEat(possCoord[0],possCoord[1],board,p1Flag):
                moves.append(possCoord)
            consecFlag = not consecFlag
    return moves

#bishop function which uses a helper to get all moves in all 4 directions
def bishop(board,position,p1Flag):
    rows,cols = len(board),len(board[0])
    pieceRow,pieceCol,piece = pieceInfo(board,position,p1Flag)
    directions = [-1,1]
    moves = list()
    
    for rowDir in directions:
        for colDir in directions:
            moves += bishopMoves(board,pieceRow,pieceCol,rowDir,colDir,p1Flag)
    return movePiece(board,pieceRow,pieceCol,piece,moves)

#Returns all possible knight moves using all possible l shaped combinations
def knightMove(board,dirRow,dirCol,pieceRow,pieceCol,p1Flag):
    rows,cols = len(board),len(board[0])
    totalMove = 3
    moves = list()
    for rowMove in range(1,totalMove):
        colMove = totalMove - rowMove
        pRow = pieceRow + rowMove*dirRow
        pCol = pieceCol + colMove*dirCol
        if  0<=pRow<rows and 0<=pCol<cols and canMove(pRow,pCol,board,p1Flag):
            moves.append((pRow,pCol))
    return moves

#A knight moves in an L shape, which covers three spaces
def knight(board,position,p1Flag):
    rows,cols = len(board),len(board[0])
    pieceRow,pieceCol,piece = pieceInfo(board,position,p1Flag)
    directions = [-1,1]
    moves = list()
    for dirRow in directions:
        for dirCol in directions:
            moves += knightMove(board,dirRow,dirCol,pieceRow,pieceCol,p1Flag)

    return movePiece(board,pieceRow,pieceCol,piece,moves)

#queen is basically a bishop and a rook combined so it contains code from them
def queen(board,position,p1Flag):
    rows,cols = len(board),len(board[0])
    pieceRow,pieceCol,piece = pieceInfo(board,position,p1Flag)
    moves = list()
    directions = [-1,1]
    lines = ['row','col']
    for rowDir in directions:
        for colDir in directions:
            moves += bishopMoves(board,pieceRow,pieceCol,rowDir,colDir,p1Flag)
    for line in lines:
        for direction in directions:
            moves += rookMoves(board,line,direction,pieceRow,pieceCol,p1Flag)
    return movePiece(board,pieceRow,pieceCol,piece,moves)

#king moves in any space around it
def king(board,position,p1Flag):
    rows,cols = len(board),len(board[0])
    pieceRow,pieceCol,piece = pieceInfo(board,position,p1Flag)
    moves = list()
    directions = [-1,0,1]
    for rowDir in directions:
        for colDir in directions:
            pMove = (pieceRow+rowDir,pieceCol+colDir)
            pRow,pCol = pMove[0],pMove[1]
            if pMove != (pieceRow,pieceCol) and 0<=pRow<rows and 0<=pCol<cols: 
                if canMove(pRow,pCol,board,p1Flag):
                    moves.append(pMove)
    return movePiece(board,pieceRow,pieceCol,piece,moves)

#A help function for the confused user
def helpChess():
    print("""
Here's what you can do!

[letter][number]: chooses what piece to move. Order of characters doesn't matter
pieces:           what and whose pieces are still alive
dead:             what and whose pieces are dead
players:          returns who is playing and if they're uppercase or lowercase
board:            prints the current chess board
help:             returns a list of functions that you can do
about:            read more about simplified chess

Press enter to continue...
     """)
    input()
    

#description of simplified chess from
#https://www.chessvariants.com/invention/simplified-chess
def about():
    print("""
From https://www.chessvariants.com/invention/simplified-chess

Introduction

Simplified Chess removes thousands of years of patchwork rules from what is
at essence a very simple game. By making seven minor rule changes, the game
becomes infinitely easier to teach but loses nothing in terms of depth of play.
The fact that there are no studied openings (as of this writing) means that even
very well studied FIDE chess players will be on equal tactical and strategic
footing with more spontaneous players.

Removing rules to make a game better is nothing new. I hope you find the rules
I've removed to have resulted in a better game.

Setup

The board is like the standard 8x8 FIDE Chess board. The exception is that the 
last row is removed. This leaves a 7x8 board, with all the Black pieces moved 
forward one space. Note that this will result in the Kings both being on 
Black squares. There are no other special set up considerations.

Pieces

You only need the standard FIDE Chess 32 piece set. You do *not* need extra 
pieces for promotions.

Rules

There are seven rules. (or removal of rules...)
Actually there are seven rules removed from FIDE Chess. 
1. There is one less row. The board is 7x8 
2. There is no check/check mate. You win by King capture. 
3. There are no Draws. 
4. There is no double move for pawns. Pawns will always move one space. 
    There is no en-passant. 
5. There is no castling. 
6. A pawn may only promote to a captured piece [QRNB] and not move to the last 
    row unless there is a piece to promote to. 
7. If a player can only legally move his King or can not legally move any 
    pieces (a very rare situation), then he loses.

Press enter to continue...
""")
    input()

#The setup that initializes simplified chess
def setup():
    pieces1=['r','kn','b','q','ki','b','kn','r','p','p','p','p','p','p','p','p']
    pieces2=['R','KN','B','Q','KI','B','KN','R','P','P','P','P','P','P','P','P']
    board = makeChessBoard()
    print("Welcome to simple chess programmed by Justin Zhang!")

    player1 = input("Player 1 name: ")
    player2 = input("Player 2 name: ")
    player1 = "Player 1" if player1 == "" else player1
    player2 = "Player 2" if player2 == "" else player2

    printChessBoard()

    print(f"{player1} (lowercase) vs {player2} (uppercase)! {player1} is first")
    print("For a list of functions, type help!")
    return board,player1,pieces1,player2,pieces2

#The main function. Uses a while loop and playerflag to make the game turn based
#Decided to submit late to implement more functions
def playSimplifiedChess():
    board,player1,pieces1,player2,pieces2 = setup()
    dead1,dead2 = list(),list()
    p1Flag = True
    while 'ki' in pieces1 and 'KI' in pieces2: 
        currPlayer = player1 if p1Flag else player2
        move = input(f"{currPlayer}, what would you like to move? ")
        if 'pieces' in move:
            print(f"{player1}: {pieces1}\n{player2}: {pieces2}")
        elif 'dead' in move:
            print(f"{player1} graveyard: {dead1}\n{player2} graveyard: {dead2}")
        elif 'help' in move:
            helpChess()
            printChessBoard(board)
        elif 'board' in move:
            printChessBoard(board)
        elif 'players' in move:
            print(f"{player1} (lowercase) vs {player2} (uppercase)")
        elif 'about' in move:
            about()
            printChessBoard(board)
        
        else:
            if pieceInfo(board,move,p1Flag) != None:
                moved = whatPiece(board,move,p1Flag)
                board,pieces1,pieces2,dead1,dead2 = update(board)
                p1Flag = not p1Flag if moved != None else p1Flag
    winner=player1 if not p1Flag else player2
    print(f"{winner} wins!")


 
#################################################
# Test Functions
#################################################


def main():
    playSimplifiedChess()
    


if __name__ == '__main__':
    main()
