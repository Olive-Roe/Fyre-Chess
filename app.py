from flask import Flask, render_template, request
import engineDEV
from threading import Thread
from os import system
from time import sleep
from turbo_flask import Turbo

app = Flask(__name__)
turbo = Turbo(app)


def runGame():
    system("python3 -m engineDEV")


def start_flask_app():
    app.run(debug=False)


def update():
    with app.app_context():
        while True:
            sleep(0.25)
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
    open('logfiles/playermove.txt', 'w').close()
    open('logfiles/pmoveReady.txt', 'w').close()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/move", methods=['POST'])
def move():
    if request.method == 'POST':
        move = request.form['pmove']
        # write move to file
        with open("logfiles/playermove.txt", "w") as f:
            f.write(move)
        # tell engine move is ready
        with open("logfiles/pmoveReady.txt", "r") as f:
            # if move is ready
            if f.read() == "True":
                # wait for move to be not ready
                # (previous move entered too fast)
                while True:
                    if f.read() == "False":
                        break
        with open("logfiles/pmoveReady.txt", "w") as f:
            # set it to ready
            f.write("True")
        # clear html form
        turbo.push(turbo.update(
            '<input type="text" name="pmove" autocomplete="off" id="moveInput" autofocus/><button id="btn" type="submit">Play move</button>', "moveInputForm"))
        return render_template("index.html")


clear_tempfiles()
t1 = Thread(target=runGame)
t2 = Thread(target=start_flask_app)
t3 = Thread(target=update)
t1.start()
t2.start()
t3.start()
