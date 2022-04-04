from flask import Flask, render_template
import engineDEV
from chess import Board
app = Flask(__name__)

b = engineDEV.BOARD
outputBoard = engineDEV.outputBoard
engineDEV.playAgainstPlayer(startingBoard=b)


@app.route("/")
def index():
    global b
    return render_template("index.html", board=b.fen())
