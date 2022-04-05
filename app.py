from flask import Flask, render_template, request
import engineDEV
import chess.svg
import threading
import os
import random

app = Flask(__name__)
outputBoard = engineDEV.outputBoard


def runGame():
    os.system("python3 -m engineDEV")


def start_flask_app():
    app.run(debug=False)


t1 = threading.Thread(target=runGame)
t2 = threading.Thread(target=start_flask_app)
t1.start()
t2.start()


@app.route("/")
def index():
    with open("logfiles/xmlboard.txt", "r") as f:
        svg = f.read()
    with open("logfiles/livePGN.txt", "r") as f:
        pgn = f.read()
    with open("logfiles/evaluation.txt", "r") as f:
        currentEval = f.read()
    return render_template("index.html", board=svg, livePGN=pgn, evaluation=currentEval)


@app.route("/xmlboard.txt")
def index():
    if request.method == "GET":
        with open("logfiles/xmlboard.txt", "r") as f:
            return f.read()
