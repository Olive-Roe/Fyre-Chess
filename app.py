from flask import Flask, render_template, request
import engineDEV
import threading
import os
import time
from turbo_flask import Turbo

app = Flask(__name__)
turbo = Turbo(app)
outputBoard = engineDEV.outputBoard


def runGame():
    os.system("python3 -m engineDEV")


def start_flask_app():
    app.run(debug=False)


def update():
    with app.app_context():
        while True:
            time.sleep(1)
            with open("logfiles/xmlboard.txt", "r") as f:
                svg = f.read()
            with open("logfiles/livePGN.txt", "r") as f:
                pgn = f.read()
            with open("logfiles/evaluation.txt", "r") as f:
                currentEval = f.read()
            turbo.push([turbo.update(svg, 'board'), turbo.update(
                pgn, 'pgn'), turbo.update(currentEval, 'eval')])


def clear_tempfiles():
    open('logfiles/evaluation.txt', 'w').close()
    open('logfiles/livePGN.txt', 'w').close()
    open('logfiles/xmlboard.txt', 'w').close()


@app.route("/")
def index():
    # return render_template("index.html", board=svg, livePGN=pgn, evaluation=currentEval)
    return render_template("index.html")


@app.route("/xmlboard.txt")
def xmlboard():
    if request.method == "GET":
        with open("logfiles/xmlboard.txt", "r") as f:
            return f.read()


clear_tempfiles()
t1 = threading.Thread(target=runGame)
t2 = threading.Thread(target=start_flask_app)
t3 = threading.Thread(target=update)
t1.start()
t2.start()
t3.start()
