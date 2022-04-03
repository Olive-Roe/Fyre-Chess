# FyreChess 1.3


from time import time
from chess import Move, Board, Piece
from random import choice


def returnBoard(move, board):
    b = Board(boardToParseableBoard(board))
    b.push(move)
    return b


def createBoardTree(board):
    legalMoves = list(board.legal_moves)
    return {i: returnBoard(i, board) for i in legalMoves}


def boardToString(board):
    "Converts a board into a string from the exact same board."
    if type(board) == Board:
        return "".join(list(str([board]))[1:][:-1])
    elif type(board) == str:
        return board
    else:
        raise ValueError(
            "boardToString was given an input that is neither a 'chess.Board' or a string")


def boardToParseableBoard(board):
    "Returns an FEN from a board."
    return "".join(list(str([board]))[8:][:-3])


pieceToSymbols = {"P": [1, True], "N": [2, True], "B": [3, True], "R": [4, True], "Q": [5, True], "K": [6, True],
                  "p": [1, False], "n": [2, False], "b": [3, False], "r": [4, False], "q": [5, False], "k": [6, False]}


def symPrint(board):
    "Returns a board printed with pieces as unicode symbols."
    outputList = []
    stringBoard = "".join(boardToParseableBoard(board).split(" ")[0])
    for symbol in stringBoard:
        if symbol in pieceToSymbols:
            pList = pieceToSymbols[symbol]
            outputList.append(Piece(pList[0], pList[1]).unicode_symbol())
        elif symbol == "/":
            outputList.append("/")
        else:  # symbol is a number and represents blank spaces
            for _ in range(int(symbol)):
                outputList.append(u"\u3000")
    return " " + "\n".join((" ".join(outputList)).split("/"))


def symbolPrint(board):
    return board  # change to symPrint for ASCII printing


positions = [11, 12, 13, 14, 15, 16, 17, 18, "", 21, 22, 23, 24, 25, 26, 27, 28, "", 31, 32, 33, 34, 35, 36, 37, 38, "", 41, 42, 43, 44, 45, 46, 47,
             48, "", 51, 52, 53, 54, 55, 56, 57, 58, "", 61, 62, 63, 64, 65, 66, 67, 68, "", 71, 72, 73, 74, 75, 76, 77, 78, "", 81, 82, 83, 84, 85, 86, 87, 88]

pieceValues = {'R': 5, 'B': 3, 'N': 3, 'K': 0, 'Q': 9, 'P': 1,
               'r': -5, 'b': -3, 'n': -3, 'k': 0, 'q': -9, 'p': -1}


def flip(pieceSquareTable):
    return pieceSquareTable[-8:] + pieceSquareTable[-16:-8] + pieceSquareTable[-24:-16] + pieceSquareTable[-32:-24] + pieceSquareTable[-40:-32] + pieceSquareTable[-48:-40] + pieceSquareTable[-56:-48] + pieceSquareTable[-64:-56]


oliOpen = {"": ["e4", "e4", "d4", "d4", "c4"],
           "e4": ["e6", "c5", "e5", "c6", "d5", "Nf6"],
           "e4 e6": ["d4"],
           "e4 e6 d4": ["d5"],
           "e4 e6 d4 d5": ["e5", "exd5"],
           "e4 e6 d4 d5 e5": ["c5"],
           "e4 e6 d4 d5 e5 c5": ["c3"],
           "e4 e5": ["Nf3"],
           "e4 e5 Nf3": ["Nc6"],
           "e4 e5 Nf3 Nc6": ["Bb5", "Bc4", "d4"],
           "e4 e5 Nf3 Nc6 Bb5": ["a6", "Nf6"],
           "e4 e5 Nf3 Nc6 Bb5 a6": ["Ba4", "Bxc6"],
           "e4 e5 Nf3 Nc6 Bc4": ["Bc5", "Nf6"],
           "e4 e5 Nf3 Nc6 d4": ["exd4"],
           "e4 c5": ["Nf3"],
           "e4 c5 Nf3": ["Nc6"],
           "e4 c5 Nf3 Nc6": ["d4"],
           "e4 c5 Nf3 Nc6 d4": ["cxd4"],
           "e4 c5 Nf3 Nc6 d4 cxd4": ["Nxd4"],
           "e4 c5 Nf3 Nc6 d4 cxd4 Nxd4": ["Nf6"],
           "e4 c5 Nf3 Nc6 d4 cxd4 Nxd4 Nf6": ["Nc3"],
           "e4 c6": ["d4", "Nc3"],
           "e4 c6 d4": ["d5"],
           "e4 c6 Nc3": ["d5"],
           "e4 c6 c4": ["d5"],
           "e4 c6 Nf3": ["d5"],
           "e4 c6 d4 d5": ["Nc3", "e5"],
           "e4 c6 d4 d5 Nc3": ["dxe4"],
           "e4 c6 d4 d5 Nc3 dxe4": ["Nxe4"],
           "e4 c6 d4 d5 Nc3 dxe4 Nxe4": ["Bf5", "Nf6"],
           "e4 d5": ["exd5"],
           "e4 d5 exd5": ["Qxd5"],
           "e4 d5 exd5 Qxd5": ["Nc3"],
           "e4 d5 exd5 Qxd5 Nc3": ["Qa5", "Qd6", "Qd8"],
           "e4 Nf6": ["e5", "Nc3"],
           "d4": ["d5", "Nf6"],
           "d4 Nf6": ["c4", "Bf4"],
           "d4 Nf6 c4": ["c5", "e6", "g6"],
           "d4 Nf6 c4 c5": ["d5"],
           "d4 d5": ["c4", "Bf4", "Nf3"],
           "d4 d5 Bf4": ["Nf6", "c5", "e6"],
           "d4 d5 Bf4 c5": ["e3"],
           "d4 d5 Bf4 c5 e3": ["Nc6"],
           "d4 d5 Bf4 c5 e3 Nc6": ["c3"],
           "d4 d5 Bf4 e6": ["Nf3", "c3", "Nd2", "e3"],
           "d4 d5 c4": ["e6"],
           "d4 d5 c4 e6": ["Nc3", "cxd5"],
           "d4 d5 c4 e6 Nc3": ["Nf6"],
           "d4 d5 c4 e6 Nc3 Nf6": ["Bg5"],
           "d4 d5 c4 e6 Nc3 Nf6 Bg5": ["Be7"],
           "d4 d5 Nf3": ["Nf6", "e6", "c6"],
           "c4": ["c5", "Nf6"],
           "c4 c5": ["Nf3", "Nc3", "g3"],
           "c4 Nf6": ["Nc3", "g3"], }


def openingMove(board):
    outputList = []
    moveStack = board.move_stack
    if moveStack == [] and board != Board():  # if moves are empty and not starting board
        return False  # check this for errors in the future
    tempMoveStack = moveStack.copy()
    for x in range(len(moveStack)):
        board.pop()
        outputList.append(board.san(tempMoveStack[-x-1]))
    for move in tempMoveStack:
        board.push(move)
    outputList.reverse()
    moves = " ".join(outputList)
    if moves in list(oliOpen.keys()):
        # dictionary lookup
        return [board.parse_san(x) for x in oliOpen[moves]]
    else:
        return False


def getPGN(moveList, board):
    "Converts a list of moves into a PGN."
    output = []
    for index, move in enumerate(moveList):
        if index % 2 == 0:  # index is even (white's move)
            output.append(f'{int(index/2 + 1)}.')
        output.append(move)
    return " ".join(output)


def convertPGNtoMoves(pgn):
    "Converts a PGN into a list of moves."
    moveList = pgn.split(" ")
    moveList2 = moveList[::3]
    for index, item in enumerate(moveList):
        if item in moveList2:
            moveList.pop(index)
    return moveList


def getBoardfromPGN(pgn):
    "From a series of moves, returns the board after the last move."
    b = Board()
    moveList = convertPGNtoMoves(pgn)
    for move in moveList:
        b.push_san(move)
    return b


def giveTurnColor(board):
    "Takes a board and returns 'w' or 'b' for the player to move."
    b = boardToParseableBoard(board).split(" ")
    return b[1]


# Piece-Square Tables
whitePawn = [0,  0,  0,  0,  0,  0,  0,  0, 50, 50, 50, 50, 50, 50, 50, 50, 10, 10, 20, 30, 30, 20, 10, 10, 5,  5, 10, 25, 25, 10,  5,
             5, 0,  0,  0, 20, 20,  0,  0,  0, 5, -5, -10,  0,  0, -10, -5,  5, 5, 10, 10, -20, -20, 10, 10,  5, 0,  0,  0,  0,  0,  0,  0,  0]
whiteKnight = [-50, -40, -30, -30, -30, -30, -40, -50, -40, -20,  0,  0,  0,  0, -20, -40, -30,  0, 10, 15, 15, 10,  0, -30, -30,  5, 15, 20, 20, 15,
               5, -30, -30,  0, 15, 20, 20, 15,  0, -30, -30,  5, 10, 15, 15, 10,  5, -30, -40, -20,  0,  5,  5,  0, -20, -40, -50, -40, -30, -30, -30, -30, -40, -50]
whiteBishop = [-20, -10, -10, -10, -10, -10, -10, -20, -10,  0,  0,  0,  0,  0,  0, -10, -10,  0,  5, 10, 10,  5,  0, -10, -10,  5,  5, 10, 10,  5,
               5, -10, -10,  0, 10, 10, 10, 10,  0, -10, -10, 10, 10, 10, 10, 10, 10, -10, -10,  5,  0,  0,  0,  0,  5, -10, -20, -10, -10, -10, -10, -10, -10, -20]
whiteRook = [0,  0,  0,  0,  0,  0,  0,  0,  5, 10, 10, 10, 10, 10, 10,  5, -5,  0,  0,  0,  0,  0,  0, -5, -5,  0,  0,  0,  0,  0,
             0, -5, -5,  0,  0,  0,  0,  0,  0, -5, -5,  0,  0,  0,  0,  0,  0, -5, -5,  0,  0,  0,  0,  0,  0, -5,  0,  0,  0,  5,  5,  0,  0,  0]
whiteQueen = [-20, -10, -10, -5, -5, -10, -10, -20, -10,  0,  0,  0,  0,  0,  0, -10, -10,  0,  5,  5,  5,  5,  0, -10, -5,  0,  5,  5,  5,  5,
              0, -5,  0,  0,  5,  5,  5,  5,  0, -5, -10,  5,  5,  5,  5,  5,  0, -10, -10,  0,  5,  0,  0,  0,  0, -10, -20, -10, -10, -5, -5, -10, -10, -20]
whiteKingMid = [-30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -50, -40, -40, -30, -30, -40, -40, -50, -
                50, -40, -40, -30, -20, -30, -30, -40, -40, -30, -30, -20, -10, -20, -20, -20, -20, -20, -20, -10, 20, 20,  0,  0,  0,  0, 20, 20, 20, 30, 10,  0,  0, 10, 30, 20]
whiteKingEnd = [-50, -40, -30, -20, -20, -30, -40, -50, -30, -20, -10,  0,  0, -10, -20, -30, -30, -10, 20, 30, 30, 20, -10, -30, -30, -10, 30, 40, 40, 30, -
                10, -30, -30, -10, 30, 40, 40, 30, -10, -30, -30, -10, 20, 30, 30, 20, -10, -30, -30, -30,  0,  0,  0,  0, -30, -30, -50, -30, -30, -30, -30, -30, -30, -50]
blackPawn = flip(whitePawn)
blackKnight = flip(whiteKnight)
blackBishop = flip(whiteBishop)
blackRook = flip(whiteRook)
blackQueen = flip(whiteQueen)
blackKingMid = flip(whiteKingMid)
blackKingEnd = flip(whiteKingEnd)


def checkMaterial(board):
    listBoard = []
    for space in boardToParseableBoard(board).split(" ")[0]:
        if space in ['1', '2', '3', '4', '5', '6', '7', '8']:
            listBoard.extend(" " for _ in range(int(space)))
        else:
            listBoard.append(space)
    whiteMaterial = 0
    blackMaterial = 0
    for piece in listBoard:
        if piece in pieceValues:
            if piece.lower() == piece:  # piece is black
                blackMaterial += pieceValues[piece]
            if piece.upper() == piece:  # piece is white
                whiteMaterial += pieceValues[piece]
    return whiteMaterial, blackMaterial


def checkIfEndgame(board):
    w, b = checkMaterial(board)
    return w <= 13 or b >= -13


def positionEvaluation(piece, pos, isEndgame):
    positionalValue = 0
    if piece == "R":
        positionalValue += (whiteRook[pos]/100)
    elif piece == "B":
        positionalValue += (whiteBishop[pos]/100)
    elif piece == "N":
        positionalValue += (whiteKnight[pos]/100)
    elif piece == "Q":
        positionalValue += (whiteQueen[pos]/100)
    elif piece == "K":
        if isEndgame == True:
            positionalValue += (whiteKingEnd[pos]/100)
        elif isEndgame == False:
            positionalValue += (whiteKingMid[pos]/100)
        else:
            raise ValueError("isEndgame is not a bool")
    elif piece == "P":
        positionalValue += (whitePawn[pos]/100)
    elif piece == "r":
        positionalValue -= (blackRook[pos]/100)
    elif piece == "b":
        positionalValue -= (blackBishop[pos]/100)
    elif piece == "n":
        positionalValue -= (blackKnight[pos]/100)
    elif piece == "q":
        positionalValue -= (blackQueen[pos]/100)
    elif piece == "k":
        if isEndgame == True:
            positionalValue -= (blackKingEnd[pos]/100)
        elif isEndgame == False:
            positionalValue -= (blackKingMid[pos]/100)
        else:
            raise ValueError("isEndgame is not a bool")
    elif piece == "p":
        positionalValue -= (blackPawn[pos]/100)
    else:
        raise ValueError("piece given is not a piece")
    #print(piece, pos, positionalValue)
    return positionalValue


def evaluate(board):
    if board.is_game_over():  # checking whether game is ended in this position
        if board.result() == "1/2-1/2":
            return 0  # drawn evaluation
        else:
            if board.turn:
                return float('-inf')
            else:
                return float('inf')
    listBoard = []
    for space in boardToParseableBoard(board).split(" ")[0]:
        if space in ['1', '2', '3', '4', '5', '6', '7', '8']:
            for x in range(int(space)):
                listBoard.append(" ")
        else:
            listBoard.append(space)
    material = 0
    counter = 0
    for piece in listBoard:
        if piece in pieceValues:
            material += pieceValues[piece]
            material += positionEvaluation(piece,
                                           counter, checkIfEndgame(board))
        if piece != "/":
            counter += 1
    material = round(material, 2)
    return float(material)
# def alphabeta(node, depth, α, β, maximizingPlayer):
# if depth == 0:
# return float(evaluate(node))
##    boardTree = createBoardTree(node)
# if maximizingPlayer:
##        value = float("-inf")
# for child in boardTree.values():
##            value = max(value, alphabeta(child, depth - 1, α, β, False))
##            α = max(α, value)
# if α >= β:
# break
# return float(value)
# else:
##        value = float("inf")
# for child in boardTree.values():
##            value = min(value, alphabeta(child, depth - 1, α, β, True))
##            β = min(β, value)
# if β <= α:
# break
# return float(value)
##
##print(alphabeta(Board(), 2, float("-inf"), float("inf"), True))
##


def isCapture(board, move):
    w1, b1 = checkMaterial(board)
    b = Board(boardToParseableBoard(board))
    b.push(move)
    w2, b2 = checkMaterial(b)
    return w1 != w2 or b1 != b2


inOpening = True
moveProgress = []


def evaluateDeep0(board, depth, tree, capture=False):
    capture = False
    global inOpening
    if inOpening:
        oMove = openingMove(board)
        if oMove != False:
            return [(choice(oMove), 0)]
        else:
            inOpening = False
    if board.is_game_over():
        if board.result() == "1/2-1/2":
            return [("", 0)]  # drawn evaluation
        else:
            if board.turn:
                return [("", float('-inf'))]
            else:
                return [("", float('inf'))]
    if depth == 0 and capture != True:
        if boardToString(board) in tree:
            return tree[boardToString(board)][1]
        else:
            return [("", evaluate(board))]
    outputList = {}
    boardTree = createBoardTree(board)
    randomMove = choice([a for a in boardTree])
    if depth == 0 and capture == True:
        highestPairs = [(randomMove, float(evaluateDeep(
            boardTree[randomMove], depth, tree)[0][1]))]
    else:
        highestPairs = [(randomMove, float(evaluateDeep(
            boardTree[randomMove], depth-1, tree)[0][1]))]
    evalList = []
    for move in boardTree:
        ##        condition = True
        if board.turn:
            condition = float(evaluate(boardTree[move])) > float(
                evaluate(board))
        else:
            condition = float(evaluate(boardTree[move])) < float(
                evaluate(board))
        if condition:
            boardState = boardTree[move]
            captureBool = isCapture(board, move)
            if depth == 0 and capture == True:
                evaluation = float(evaluateDeep(
                    boardState, depth, tree, capture=captureBool)[0][1])
            else:
                evaluation = float(evaluateDeep(
                    boardState, depth-1, tree, capture=captureBool)[0][1])  # recursion
            evalList.append(evaluation)
            highestVal = highestPairs[0][1]
            if evaluation == highestVal and move not in [highestPairs[x][0] for x in range(0, len(highestPairs))]:
                highestPairs.append((move, evaluation))
            else:
                if board.turn:
                    if evaluation > highestVal:
                        highestPairs = [(move, evaluation)]
                else:
                    if evaluation < highestVal:
                        highestPairs = [(move, evaluation)]
    tree[boardToString(board)] = [boardTree, highestPairs]
    return highestPairs


def evaluateDeep(board: Board, depth: int, tree: dict, capture=False):
    global moveProgress
    global inOpening
    if depth == 2:
        moveProgress = []
    if inOpening:
        oMove = openingMove(board)
        if oMove != False:
            return [(choice(oMove), 0)]
        else:
            inOpening = False
    if board.is_game_over():
        if board.result() == "1/2-1/2":
            tree[boardToString(board)] = [("", 0)]
            return [("", 0)]  # drawn evaluation
        else:
            if board.turn:
                tree[boardToString(board)] = [("", float('-inf'))]
                return [("", float('-inf'))]
            else:
                tree[boardToString(board)] = [("", float('inf'))]
                return [("", float('inf'))]

    #print("Wahoo, new board, ", depth, capture)
    if depth == 0:
        if capture == False:
            ##            print(" ".join(moveProgress))
            ##            moveProgress = []
            if boardToString(board) in tree:
                # print(tree[boardToString(board)])
                if type(tree[boardToString(board)][0]) == dict:
                    return tree[boardToString(board)][1]
                else:
                    return tree[boardToString(board)]
            else:
                tree[boardToString(board)] = [("", evaluate(board))]
                return [("", evaluate(board))]
    outputList = {}
    boardTree = createBoardTree(board)
    randomMove = choice([a for a in boardTree])
    if depth == 0 and capture == True:
        highestPairs = [(randomMove, float(evaluateDeep(
            boardTree[randomMove], depth, tree)[0][1]))]
        #print("captures is true yay, last depth")
    else:
        highestPairs = [(randomMove, float(evaluateDeep(
            boardTree[randomMove], depth-1, tree)[0][1]))]
    boardTree.pop(randomMove)  # testing whether this is more efficient
    evalList = []
    for move in boardTree:
        ##        condition = True
        if board.turn:
            condition = float(evaluate(boardTree[move])) > float(
                evaluate(board))
        else:
            condition = float(evaluate(boardTree[move])) < float(
                evaluate(board))
        if condition:
            # moveProgress.append(str(move))
            # moveProgress.append(depth)
            boardState = boardTree[move]
            captureBool = isCapture(board, move)
            #print("capture is true", move, depth)
            if depth == 0:
                if capture == True:
                    #print("capturebool is true, last depth", move, depth)
                    evaluation = float(evaluateDeep(
                        boardState, 0, tree, captureBool)[0][1])
                else:
                    raise SyntaxError("this shouldn't happen")
            else:
                #print("depth is not 0", captureBool, capture)
                evaluation = float(evaluateDeep(
                    boardState, depth-1, tree, captureBool)[0][1])  # recursion
            evalList.append(evaluation)
            highestVal = highestPairs[0][1]
            if evaluation == highestVal and move not in [highestPairs[x][0] for x in range(0, len(highestPairs))]:
                highestPairs.append((move, evaluation))
            else:
                if board.turn:
                    if evaluation > highestVal:
                        highestPairs = [(move, evaluation)]
                else:
                    if evaluation < highestVal:
                        highestPairs = [(move, evaluation)]
    tree[boardToString(board)] = [boardTree, highestPairs]
    return highestPairs


def evaluateDeep2(board, depth, tree, capture=False, alpha=float('-inf'), beta=float('inf')):
    global moveProgress
    global inOpening
    if depth == 2:
        moveProgress = []
    if inOpening:
        oMove = openingMove(board)
        if oMove != False:
            return [(choice(oMove), 0)]
        else:
            inOpening = False
    if board.is_game_over():
        if board.result() == "1/2-1/2":
            tree[boardToString(board)] = [("", 0)]
            return [("", 0)]  # drawn evaluation
        else:
            if board.turn:
                tree[boardToString(board)] = [("", float('-inf'))]
                return [("", float('-inf'))]
            else:
                tree[boardToString(board)] = [("", float('inf'))]
                return [("", float('inf'))]

    if depth == 0:
        if capture == False:
            if boardToString(board) in tree:
                if type(tree[boardToString(board)][0]) == dict:
                    return tree[boardToString(board)][1]
                else:
                    return tree[boardToString(board)]
            else:
                tree[boardToString(board)] = [("", evaluate(board))]
                return [("", evaluate(board))]
    outputList = {}
    boardTree = createBoardTree(board)
    randomMove = choice([a for a in boardTree])
    if depth == 0 and capture == True:
        highestPairs = [(randomMove, float(evaluateDeep(
            boardTree[randomMove], depth, tree)[0][1]))]
    else:
        highestPairs = [(randomMove, float(evaluateDeep(
            boardTree[randomMove], depth-1, tree)[0][1]))]
    boardTree.pop(randomMove)
    evalList = []
    for move in boardTree:
        if board.turn:
            condition = float(evaluate(boardTree[move])) > float(
                evaluate(board))
        else:
            condition = float(evaluate(boardTree[move])) < float(
                evaluate(board))
        if condition:
            boardState = boardTree[move]
            captureBool = isCapture(board, move)
            if depth == 0:
                if capture == True:
                    evaluation = float(evaluateDeep(
                        boardState, 0, tree, captureBool)[0][1])
                else:
                    raise SyntaxError("this shouldn't happen")
            else:
                evaluation = float(evaluateDeep(
                    boardState, depth-1, tree, captureBool)[0][1])  # recursion
            evalList.append(evaluation)
            highestVal = highestPairs[0][1]
            if evaluation == highestVal and move not in [highestPairs[x][0] for x in range(0, len(highestPairs))]:
                highestPairs.append((move, evaluation))
            else:
                if board.turn:
                    if evaluation > highestVal:
                        highestPairs = [(move, evaluation)]
                else:
                    if evaluation < highestVal:
                        highestPairs = [(move, evaluation)]
    tree[boardToString(board)] = [boardTree, highestPairs]
    return highestPairs


def evaluateDeep3(board: Board, depth: int, forcing=False, alpha=float('-inf'), beta=float('inf')):  # does not work yet
    '''returns (evaluation, move) of the best move'''
    # game over checks
    if board.is_game_over():
        if board.result() == "1/2-1/2":
            return (0, "")  # draw
        elif board.turn:
            return (float('-inf'), "")  # black wins
        else:
            return (float('inf'), "")  # white wins
    if depth == 0:
        return (evaluate(board), "")
    if depth != 0:
        firstRepetition = True
        boardTree = createBoardTree(board)
        for move in boardTree:
            boardState = boardTree[move]
            evaluation, move1 = evaluateDeep3(boardState, depth-1)
            # print(depth-1, move, evaluation, end=", ")
            if evaluation == float('inf') and board.turn:
                return (float('inf'), move)
            elif evaluation == float('-inf') and (not board.turn):
                return (float('-inf'), move)
            if firstRepetition == True:
                bestEval = evaluation
                bestMove = move
                firstRepetition = False
            # if it's white's move and the current move is better than the best move,
            elif board.turn and evaluation > bestEval:
                bestMove = move
                bestEval = evaluation
            # or if it's black's move,
            elif (board.turn) == False and evaluation < bestEval:
                bestMove = move
                bestEval = evaluation
            print("finally, ", depth, move, evaluation, end=", ")
        return evaluation, bestMove


def evaluateDeep4(board: Board, depth, tree, inOpening=False, alpha=float("-inf"), beta=float("inf"), maximising=True):
    # FIXME: plays a pretty bad move tbh
    if inOpening:
        oMove = openingMove(board)
        if oMove != False:
            return 0, choice(oMove)
        else:
            inOpening = False
    if board.is_game_over():
        if board.result() == "1/2-1/2":
            return 0, ""  # draw
        elif board.turn:
            return float('-inf'), ""  # black wins
        else:
            return float('inf'), ""  # white wins
    if depth == 0:
        return evaluate(board), ""
    if maximising:  # computer to move
        maxEval = float("-inf")
        bestMove = ""
        boardTree = createBoardTree(board)
        for move in boardTree:
            evaluation, newmove = evaluateDeep4(
                boardTree[move], depth - 1, tree, inOpening, alpha, beta, False)
            if evaluation > maxEval:
                maxEval = evaluation
                bestMove = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break  # prune
        return evaluation, bestMove
    # player to move
    minEval = float("inf")
    bestMove = ""
    boardTree = createBoardTree(board)
    for move in boardTree:
        evaluation, newmove = evaluateDeep4(
            boardTree[move], depth - 1, tree, inOpening, alpha, beta, True)
        if evaluation < minEval:
            minEval = evaluation
            bestMove = move
        beta = min(beta, evaluation)
        if beta <= alpha:
            break  # prune the tree, better option somewhere else
    return evaluation, bestMove


def evaluateThisv1(board, tree):
    moves = evaluateDeep0(board, 2, tree)
    if moves != None:
        move, evaluation = choice(moves)
        print(moves)
        return evaluation, move


def evaluateThisv2(board, tree):
    moves = evaluateDeep2(board, 2, tree)
    if moves != None:
        move, evaluation = choice(moves)
        print(moves)
        return evaluation, move


def evaluateThisv3(board, tree):  # not working yet
    return evaluateDeep3(board, 2)


def evaluateThisv4(board, tree, inOpening):
    return evaluateDeep4(board, 2, tree, inOpening, maximising=board.turn)


def playAgainstPlayer(computerColor="w", startingBoard=Board, tree={}):
    global outputBoard
    moveList = []
    timeList = []
    gamesList = []
    b = startingBoard
    t = tree
    move = ""
    inOpening = True
    starting = giveTurnColor(startingBoard)

    def endCheck(board: Board):
        return board.is_game_over()

    def end(board: Board):
        if board.is_game_over:
            if board.result() == "1/2-1/2":
                return "Draw"
            return "Black wins" if board.turn else "White wins"

    def computerMove3():  # new version
        start = time()
        move = ""
        while True:
            try:
                a = evaluateThisv4(b, t, inOpening)
                if a != None:
                    evaluation, move = a
                    break
            except ValueError:
                print(f"Invalid move: {move} in board {b}")
                continue
        print(b.san(move))
        moveList.append(b.san(move))
        b.push(move)
        end = time()
        timeList.append(round(end - start, 3))
        print(symbolPrint(b), move, evaluation, timeList[-1], "\n")

    def humanMove():
        while True:
            try:
                inp = input("\n What do you move? ")
                b.push_san(inp)
                print(symbolPrint(b), evaluate(b), "\n")
                break
            except ValueError:
                if inp.lower() == "undo":
                    print("Undoing...")
                    b.pop()
                    b.pop()
                    moveList.pop(moveList[-1])
                    moveList.pop(moveList[-1])
                elif inp.lower() == "time":
                    print(f"Time taken on last move: {timeList[-1]}")
                    print(f"Time for every move: {timeList}")
                else:
                    print("Invalid move.")
                continue
        moveList.append(inp)

    gameType = ""
    while gameType not in ["c", "p"]:
        gameType = input(
            "\nEnter p for player vs computer, and c for computer vs computer: ")
    if gameType == "c":
        def cMove():
            computerMove3()
            print(getPGN(moveList, b))
            if endCheck(b):
                return False

        def result(wScore, bScore, board):
            if board.result() == "1-0":
                wScore += 1
            elif board.result() == "0-1":
                bScore += 1
            elif board.result() == "1/2-1/2":
                wScore += 0.5
                bScore += 0.5
            else:
                raise ValueError("board.result returned unexpected value")
            return wScore, bScore
        times = int(input("How many times do you want them to play? "))
        wScore, bScore = 0, 0
        for i in range(times):
            b.reset()
            inOpening = True
            moveList = []
            while True:
                if cMove() == False:
                    break
            wScore, bScore = result(wScore, bScore, b)
            print(f"Computer 1: {wScore} Computer 2: {bScore}")
            gamesList.append(getPGN(moveList, b))
            print(gamesList)

    elif gameType == "p":
        print(f"Starting Game:\n{symbolPrint(b)}")

        def white():
            if computerColor == "w":
                computerMove3()
            else:
                humanMove()
            print(getPGN(moveList, b))
            if endCheck(b):
                return False

        def black():
            if computerColor == "b":
                computerMove3()
            else:
                humanMove()
            print(getPGN(moveList, b))
            if endCheck(b):
                return False
        if starting == "w":  # white to play
            inOpening = True
            white()
        while True:  # black to play goes to this
            if black() == False:
                break
            if white() == False:
                break
        print(end(b))  # end message to show who won
        print(timeList)
        print(getPGN(moveList, b))


if __name__ == "__main__":
    board1 = Board('4r1k1/ppp2ppp/4b3/4Q3/3p2B1/1P1P4/P4PPP/2R3K1 b - - 1 20')
    board2 = Board(
        'rnbqkb1r/pppppppp/5n2/8/4P3/2N5/PPPP1PPP/R1BQKBNR b KQkq - 2 2')
    masterTree = {}
    playAgainstPlayer("b", Board(), masterTree)

outputBoard = ""
BOARD = Board()

'''
[Event "FyreChess Plays Against Itself"]

[Site "Oliver's House"]
[Date "2021.2.23"]
[Round "?"]
[White "FyreChess 1.3"]
[Black "FyreChess 1.3"]
[Result "1-0"]


'''

# Additions in 1.3
'''
Added game_over checks to evaluate()
Gave some functions descriptions
Created functions 'getPGN, convertPGNtoMoves, getBoardfromPGN, giveTurnColor'
Made mainloop able to start from positions with black to play
Changed openingMove not work with a set position that is not the starting position.
Changed capturing depth to work now, but it is much slower
Fixed some errors in opening book
Made symbolPrint work better with unicode spaces
'''
