from flask import Flask, render_template, request
import engineDEV
import chess.svg
app = Flask(__name__)
b = engineDEV.BOARD
outputBoard = engineDEV.outputBoard


@app.route("/")
def index():
    if request.method == 'GET':  # displaying board
        return chess.svg.board(b, size=600)
    else:  # loading page
        return render_template("index.html", board=chess.svg.board(b, size=600))


if __name__ == "__main__":
    app.run(debug=True)
    engineDEV.playAgainstPlayer(startingBoard=b)
