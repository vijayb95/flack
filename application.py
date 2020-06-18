import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_socketio import SocketIO, emit
from functools import wraps
from helpers import apology, name_required


app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

app.config["TEMPLATES_AUTO_RELOAD"] = True
messages = {}
channelList = []


@app.route("/")
@name_required
def index():
    if session["user_id"] == None:
        return redirect("/getName")
    else:
        return render_template("index.html", channels = channelList)

@app.route("/getName", methods=["GET", "POST"])
def userName():
    session.clear()

    if request.method == "POST":
        
        if not request.form.get("username"):
            return apology("Please type your name", 403)

        session["user_id"] = request.form.get("username")

        return redirect("/")

    else:
        return render_template("getName.html")

@socketio.on("submit group")
def group(data):
    if data["group"] != "":
        channelList.append(data["group"])
        messages.update(data["group"])
        emit("channels", channelList, broadcast=True)

@socketio.on("messages")
def mess(data):
    message = messages[data["selection"]]
    emit("message", message, broadcast=True)







