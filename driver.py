from app import turbo as turbo
from app import app as webapp
from engineDEV import giveTurnColor, getPGN, evaluateThis, symbolPrint, formatPGN
from chess import Board, WHITE, BLACK
from chess import svg as svg
from threading import Thread
from time import time


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


def playAgainstPlayer(computerColor="b", startingBoard=Board(), tree=None, fromWeb=True, gameType="c", rounds=1):
    moveList = []
    timeList = []
    gamesList = []
    pgn = ""
    b = startingBoard
    t = {} if tree == None else tree
    inOpening = True
    starting = giveTurnColor(startingBoard)

    def localUpdatePage(evaluation="-"):
        updatePage(evaluation, moveList, b)

    localUpdatePage()

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
            raise e
        b.push(move)
        end = time()
        timeList.append(round(end - start, 3))
        print(
            f"{symbolPrint(b)} \nMove: {b2.san(move)}\nEval: {evaluation}\nTime taken: {timeList[-1]}\n")
        localUpdatePage()
        return evaluation

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
                break
            except ValueError:
                if sanMove.lower() == "undo":
                    b.pop()
                    b.pop()
                    moveList.pop()
                    moveList.pop()
                    timeList.pop()
                    localUpdatePage()
                else:
                    # clear current move
                    with open("logfiles/playermove.txt", "w") as f:
                        f.write("")
                continue
        moveList.append(sanMove)
        localUpdatePage()

    if gameType == "c":
        def cMove(depth=2):
            evaluation = computerMove(depth)
            print(getPGN(moveList, b))
            if b.is_game_over():
                return "end"
            return evaluation

        times = rounds
        wScore, bScore = 0, 0
        wDepth, bDepth = 2, 2
        for i in range(times):
            b.reset()  # white will always go first here
            inOpening = True
            moveList = []
            while True:
                wEval = cMove(wDepth)
                if wEval == "end":
                    localUpdatePage(wEval)
                    break
                bEval = cMove(bDepth)
                if bEval == "end":
                    localUpdatePage(bEval)
                    break
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
        #print(f"Starting Game:\n{symbolPrint(b)}")
        depth = 2

        def white():
            if computerColor == "w":
                evaluation = computerMove(depth)
            else:
                humanMoveFromHTML()
            print(getPGN(moveList, b))
            if b.is_game_over():
                return "end"
            return evaluation if computerColor == "w" else "-"

        def black():
            if computerColor == "b":
                evaluation = computerMove(depth)
            else:
                humanMoveFromHTML()
            print(getPGN(moveList, b))
            if b.is_game_over():
                return "end"
            return evaluation if computerColor == "b" else "-"
        cScore, hScore = 0, 0
        for i in range(rounds):
            inOpening = True
            moveList = []
            b.reset()
            if starting == "w":  # white to play
                inOpening = True
                white()
            while True:  # black to play goes to this
                blackEval = black()
                if blackEval == "end":
                    localUpdatePage(blackEval)
                    break
                whiteEval = white()
                if whiteEval == "end":
                    localUpdatePage(whiteEval)
                    break
            currentPGN = getPGN(moveList, b)
            assert b.is_game_over()
            # end message to show who won
            end = "Draw" if b.result() == "1/2-1/2" else "Black wins" if b.turn else "White wins"
            print(f"{end}\n{timeList}\n{currentPGN}")
            # format pgn with round number (i from for loop)
            if computerColor == "w":
                cPGN = formatPGN(
                    currentPGN, f"FC 1.3.2 (depth {depth})", "Human", b.result(), i+1)
            else:
                cPGN = formatPGN(currentPGN, "Human",
                                 f"FC 1.3.2 (depth {depth})", b.result(), i+1)
            pgn += currentPGN
            # append latest game to gamelog
            with open("logfiles/gamelog.txt", "a") as f:
                f.write(cPGN)
            wScore, bScore = result(0, 0, b)
            cScore += wScore if computerColor == "w" else bScore
            hScore += wScore if computerColor == "b" else bScore
            print(f"Human: {hScore}, Computer: {cScore}")
            # change sides
            computerColor = "w" if computerColor == "b" else "b"


def runGame():
    b = Board()
    masterTree = {}
    playAgainstPlayer("b", b, masterTree, True, "p", 2)


def start_flask_app():
    webapp.run(debug=False)


def updatePage(evaluation, moveList, b, orientation="w"):
    if moveList is None:
        moveList = []
    orientation = WHITE if orientation == "w" else BLACK
    webSVG = svg.board(b, size=600, orientation=orientation)
    pgn = getPGN(moveList, b)
    currentEval = str(evaluation)
    with webapp.app_context():
        turbo.push([turbo.update(webSVG, 'board'), turbo.update(
            pgn, 'pgn'), turbo.update(currentEval, 'eval')])


def clear_tempfiles():
    open('logfiles/playermove.txt', 'w').close()
    open('logfiles/pmoveReady.txt', 'w').close()


t1 = Thread(target=runGame)
t2 = Thread(target=start_flask_app)

if __name__ == "__main__":
    clear_tempfiles()
    t1.start()
    t2.start()
