from flask import Flask, render_template, request
from turbo_flask import Turbo

app = Flask(__name__)
turbo = Turbo(app)


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
