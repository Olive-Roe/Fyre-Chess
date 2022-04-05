from flask import Flask, render_template, request
import engineDEV
import chess.svg
import threading
import os

app = Flask(__name__)
b = engineDEV.BOARD
outputBoard = engineDEV.outputBoard


def runGame():
    os.system("python3 -m engineDEV.py")


def start_flask_app():
    app.run(debug=False)


t1 = threading.Thread(target=runGame)
t2 = threading.Thread(target=start_flask_app)
t1.start()
t2.start()


@app.route("/")
def index():
    if request.method == 'GET':  # displaying board
        return chess.svg.board(b, size=600)
    else:  # loading page
        return render_template("index.html", board=chess.svg.board(b, size=600))
