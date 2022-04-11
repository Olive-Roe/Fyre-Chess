# FyreChess 1.3.2


from time import time
from datetime import datetime
from chess import Board, Piece
import chess.svg
from random import choice


def returnBoard(move, board):
    b = Board(boardToParseableBoard(board))
    b.push(move)
    return b


def orderBoardTree(originalBoard: Board, boardTree):
    "Heuristically orders a board tree and returns it"
    moveList = []
    checkList = []
    captureList = []
    pawnList = []
    pieceDict = {"N": [],
                 "B": [],
                 "R": [],
                 "Q": [],
                 "K": []
                 }
    for move in boardTree:
        b2 = originalBoard.copy()
        b2.push(move)
        if b2.is_game_over() and b2.result() != "1/2-1/2":
            return {move: boardTree[move]}
        if b2.is_check():
            checkList.append(move)
        san = originalBoard.san(move)
        if "=Q" in san:
            moveList.insert(0, move)
        if "x" in san:
            captureList.append(move)
        for piece, value in pieceDict.items():
            if piece in san:
                value.append(move)
                break
        else:
            # pawn move
            pawnList.append(move)
    pieceList = []
    for v in pieceDict.values():
        pieceList.extend(iter(v))
    for exList in checkList, captureList, pawnList, pieceList:
        moveList.extend(exList)
    return {k: boardTree[k] for k in moveList}


def createBoardTree(board):
    legalMoves = list(board.legal_moves)
    return orderBoardTree(board, {i: returnBoard(i, board) for i in legalMoves})


def boardToString(board):
    "Converts a board into a string from the exact same board."
    if type(board) == Board:
        return "".join(list(str([board]))[1:][:-1])
    elif type(board) == str:
        return board
    else:
        raise ValueError(
            "boardToString was given an input that is neither a 'chess.Board' or a string")


def boardToParseableBoard(board: Board):
    "Returns an FEN from a board."
    return board.fen()


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
            outputList.extend(u"\u3000" for _ in range(int(symbol)))
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


def openingMove(board):  # sourcery skip: inline-immediately-returned-variable
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
        output = [board.parse_san(x) for x in oliOpen[moves]]
        # del(oliOpen[moves])
        # deletes move from opening book (avoids repetition but creates repetition of computer's own opening)
        return output
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
    # print(piece, pos, positionalValue)
    return positionalValue


def evaluate(board):
    if board.is_game_over():  # checking whether game is ended in this position
        if board.result() == "1/2-1/2":
            return 0  # drawn evaluation
        else:
            return float('-inf') if board.turn else float('inf')
    listBoard = []
    for space in boardToParseableBoard(board).split(" ")[0]:
        if space in ['1', '2', '3', '4', '5', '6', '7', '8']:
            listBoard.extend(" " for _ in range(int(space)))
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


def isCapture(board, move):
    w1, b1 = checkMaterial(board)
    b = Board(boardToParseableBoard(board))
    b.push(move)
    w2, b2 = checkMaterial(b)
    return w1 != w2 or b1 != b2


def continueSearch(board: Board, move, condition="check"):
    "Returns True if the search should continue looking for extra depth, or not"
    # TODO: continue for +2 depth if check, so all directly forcing sequences are searched
    b2 = board.copy()
    b2.push(move)
    return b2.is_check()


def evaluateDeep(board: Board, depth, tree, inOpening=False, alpha=float("-inf"), beta=float("inf"), maximising=True, moveList=""):
    if inOpening:
        oMove = openingMove(board)
        if oMove != False:
            return 0, choice(oMove)
        else:
            # out of opening
            inOpening = False
    if board.is_game_over():
        if board.result() == "1/2-1/2":
            return 0, ""  # draw
        elif board.turn:
            return float('-inf'), ""  # black wins
        else:
            return float('inf'), ""  # white wins
    if depth == 0:
        # print(f"{'  '*(1-depth)} {moveList}: {evaluate(board)}")
        return evaluate(board), ""
    if maximising:  # white to move
        maxEval = float("-inf")
        bestMove = ""
        boardTree = createBoardTree(board)
        for move in boardTree:
            if continueSearch(board, move) and depth == 1:
                # searches with an extra depth
                evaluation, newmove = evaluateDeep(
                    boardTree[move], depth, tree, inOpening, alpha, beta, False, f"{moveList} {board.san(move)}")
            else:
                evaluation, newmove = evaluateDeep(
                    boardTree[move], depth - 1, tree, inOpening, alpha, beta, False, f"{moveList} {board.san(move)}")
            # print(f"{'  '*(1-depth)} {moveList}: {evaluation}")
            if evaluation > maxEval:
                maxEval = evaluation
                bestMove = move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break  # prune
        # print(f"{'  '*(2-depth)} Best move for white {bestMove}: {maxEval}")
        if bestMove == '':  # checkmate is unavoidable
            return float("-inf"), list(boardTree.keys())[0]  # first move
        return maxEval, bestMove
    # black to move
    minEval = float("inf")
    bestMove = ""
    boardTree = createBoardTree(board)
    for move in boardTree:
        if continueSearch(board, move) and depth == 1:
            evaluation, newmove = evaluateDeep(
                boardTree[move], depth, tree, inOpening, alpha, beta, True, f"{moveList} {board.san(move)}")
        else:
            evaluation, newmove = evaluateDeep(
                boardTree[move], depth - 1, tree, inOpening, alpha, beta, True, f"{moveList} {board.san(move)}")
        # print(f"{'  '*(1-depth)} {moveList}: {evaluation}")
        if evaluation < minEval:
            minEval = evaluation
            bestMove = move
        beta = min(beta, evaluation)
        if beta <= alpha:
            break  # prune the tree, better option somewhere else
    # print(f"{'  '*(2-depth)} Best move for black {bestMove}: {minEval}")
    if bestMove == '':  # checkmate is unavoidable
        return float("inf"), list(boardTree.keys())[0]  # first move
    return minEval, bestMove


def evaluateThis(board, tree, depth=2, inOpening=False):
    return evaluateDeep(board, depth, tree, inOpening, maximising=board.turn)


def formatPGN(pgn, player1, player2, result, roundnumber="?"):
    return f'''[Event "?"]\n[Site "?"]\n[Date "{datetime.now().strftime('%Y.%m.%d')}"]\n[Round "{roundnumber}"]\n[White "{player1}"]\n[Black "{player2}"]\n[Result "{result}"]\n\n{pgn}\n\n'''


def playAgainstPlayer(computerColor="w", startingBoard=Board(), tree={}, fromWeb=True):
    global b
    moveList = []
    timeList = []
    gamesList = []
    pgn = ""
    b = startingBoard
    t = tree
    inOpening = True
    starting = giveTurnColor(startingBoard)

    def updateFiles(evaluation="-"):
        with open("logfiles/xmlboard.txt", "w") as f:
            f.write(chess.svg.board(b, size=600))
        with open("logfiles/livePGN.txt", "w") as f:
            f.write(getPGN(moveList, b))
        with open("logfiles/evaluation.txt", "w") as f:
            f.write(str(evaluation))

    updateFiles()

    def endCheck(board: Board):
        return board.is_game_over()

    def end(board: Board):
        "Returns a end message"
        if board.is_game_over:
            if board.result() == "1/2-1/2":
                return "Draw"
            return "Black wins" if board.turn else "White wins"

    def computerMove(depth=2):
        start = time()
        move = ""
        while True:
            try:
                a = evaluateThis(b, t, depth, inOpening)
                if a != None:
                    evaluation, move = a
                    break
            except ValueError:
                print(f"Invalid move: {move} in board {b}")
                continue
        try:
            b2 = b.copy()
            moveList.append(b.san(move))
        except AttributeError as e:
            print(f"Bad move: {move} in board\n{b}")
            raise
        b.push(move)
        end = time()
        timeList.append(round(end - start, 3))
        print(
            f"{symbolPrint(b)} \nMove: {b2.san(move)}\nEval: {evaluation}\nTime taken: {timeList[-1]}\n")
        return evaluation

    def humanMove():
        while True:
            try:
                inp = input("\n What do you move? ")
                b.push_san(inp)
                print(symbolPrint(b), "\n")
                break
            except ValueError:
                if inp.lower() == "undo":
                    if moveList == []:
                        # starting position, nothing to undo
                        continue
                    print("Undoing...")
                    b.pop()
                    b.pop()
                    moveList.pop(moveList[-1])
                    moveList.pop(moveList[-1])
                    timeList.pop()
                elif inp.lower() == "time":
                    print(f"Time taken on last move: {timeList[-1]}")
                    print(f"Time for every move: {timeList}")
                else:
                    print("Invalid move.")
                continue
        moveList.append(inp)

    def getMove():
        # wait for input from client side
        while True:
            with open("logfiles/pmoveReady.txt", "r") as f:
                if f.read() == "True":
                    break
        # set move to not ready
        with open("logfiles/pmoveReady.txt", "w") as f:
            f.write("False")
        # read move
        with open("logfiles/playermove.txt", "r") as f:
            sanMove = f.read()
        return sanMove

    def humanMoveFromHTML():
        # play move
        while True:
            # runs loop until move is gotten
            if fromWeb:
                sanMove = getMove()
            else:
                inp = input("\n What do you move? ")
                b.push_san(inp)
                print(symbolPrint(b), "\n")
            try:
                b.push_san(sanMove)
                updateFiles()
                break
            except ValueError:
                if sanMove.lower() == "undo":
                    b.pop()
                    b.pop()
                    moveList.pop()
                    moveList.pop()
                    timeList.pop()
                    updateFiles()
                else:
                    # clear current move
                    with open("logfiles/playermove.txt", "w") as f:
                        f.write("")
                continue
        moveList.append(sanMove)

    gameType = ""
    while gameType not in ["c", "p"]:
        gameType = input(
            "\nEnter p for player vs computer, and c for computer vs computer: ")
    if gameType == "c":
        def cMove(depth=2):
            evaluation = computerMove(depth)
            print(getPGN(moveList, b))
            if endCheck(b):
                return "end"
            return evaluation

        def result(wScore, bScore, board):
            if board.result() == "1-0":
                wScore += 1
            elif board.result() == "0-1":
                bScore += 1
            elif board.result() == "1/2-1/2":
                wScore += 0.5
                bScore += 0.5
            else:
                raise ValueError(
                    f"Board: {board} board.result returned unexpected value")
            return wScore, bScore
        times = int(input("How many times do you want them to play? "))
        wScore, bScore = 0, 0
        wDepth, bDepth = 2, 2
        for i in range(times):
            b.reset()  # white will always go first here
            inOpening = True
            moveList = []
            while True:
                wEval = cMove(wDepth)
                if wEval == "end":
                    updateFiles(wEval)
                    break
                updateFiles(wEval)
                bEval = cMove(bDepth)
                if bEval == "end":
                    updateFiles(wEval)
                    break
                updateFiles(bEval)
            wScore, bScore = result(wScore, bScore, b)
            print(f"Computer 1: {wScore} Computer 2: {bScore}")
            currentPGN = getPGN(moveList, b)
            gamesList.append(currentPGN)
            currentFormattedPGN = formatPGN(
                currentPGN, f"FC 1.3.2 (depth {wDepth})", f"FC 1.3.2 (depth {bDepth})", b.result(), i+1)
            pgn += currentFormattedPGN
            with open("logfiles/gamelog.txt", "a") as f:
                f.write(currentFormattedPGN)
            print(gamesList)
            print(pgn)

    elif gameType == "p":
        print(f"Starting Game:\n{symbolPrint(b)}")
        depth = 2

        def white():
            if computerColor == "w":
                evaluation = computerMove(depth)
            else:
                humanMoveFromHTML()
            print(getPGN(moveList, b))
            if endCheck(b):
                return "end"
            return evaluation if computerColor == "w" else "-"

        def black():
            if computerColor == "b":
                evaluation = computerMove(depth)
            else:
                humanMoveFromHTML()
            print(getPGN(moveList, b))
            if endCheck(b):
                return "end"
            return evaluation if computerColor == "b" else "-"

        if starting == "w":  # white to play
            inOpening = True
            white()
        while True:  # black to play goes to this
            blackEval = black()
            if blackEval == "end":
                updateFiles(blackEval)
                break
            updateFiles(blackEval)
            whiteEval = white()
            if whiteEval == "end":
                updateFiles(whiteEval)
                break
            updateFiles(whiteEval)
        print(end(b))  # end message to show who won
        print(timeList)
        print(getPGN(moveList, b))
        currentPGN = getPGN(moveList, b)
        gamesList.append(currentPGN)
        wPlayer = "Human" if computerColor == "b" else f"FC 1.3.2 (depth {depth})"
        bPlayer = "Human" if computerColor == "w" else f"FC 1.3.2 (depth {depth})"
        currentFormattedPGN = formatPGN(
            currentPGN, wPlayer, bPlayer, b.result())
        pgn += currentFormattedPGN
        with open("logfiles/gamelog.txt", "a") as f:
            f.write(currentFormattedPGN)
        print(gamesList)
        print(pgn)


b = Board()
outputBoard = Board()
BOARD = Board()

if __name__ == "__main__":
    # whiteTestCases = {}
    # blackTestCases = {"bishop for mate?": '4r1k1/ppp2ppp/4b3/4Q3/3p2B1/1P1P4/P4PPP/2R3K1 b - - 1 20',
    #                   "pawn for knight?": 'rnbqkb1r/pppppppp/5n2/8/4P3/2N5/PPPP1PPP/R1BQKBNR b KQkq - 2 2',}
    masterTree = {}
    # for test in whiteTestCases:
    #     print(test)
    #     playAgainstPlayer("w", Board(whiteTestCases[test]), masterTree)
    # for test in blackTestCases:
    #     print(test)
    #     playAgainstPlayer("b", Board(blackTestCases[test]), masterTree)
    # playAgainstPlayer("b", Board(), masterTree)
    # svg = chess.svg.board(Board())
    # gui_tkinter.refreshScreen(svg)
    playAgainstPlayer("b", BOARD, masterTree)

# To-do List
'''
Create display to see the engine's current & best moves (thought process), write to file from server and display with turbo-flask
Use CSS to make everything beautiful
Decide when version 1.3.2 is finished and update engine.py to v1.3.2 (follow incompatible.compatible features.compatible fixes)?
'''

# Additions in 1.3.2
'''
Delete and improve old functions (some Sourcery refactorings as well)
Using new search function with alpha-beta pruning (evaluateDeep4)
Better output formatting
Added export PGN formatting (formatPGN)
Logging games in text file
Created heuristic move ordering function to improve efficiency (orderBoardTree)
Added function to allow search to continue with certain conditions (continueSearch)
Added custom depth for the engine
Created auto-updating web display with html, flask, turbo-flask
Format text box in index.html better, allow word wrap
Create input for the player in index.html, process with flask and play it in the server
'''

# Additions in 1.3.1
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
