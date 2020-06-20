import os

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_socketio import SocketIO, emit
from functools import wraps
from helpers import apology, name_required

app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
socketio = SocketIO(app)

# app.config["TEMPLATES_AUTO_RELOAD"] = True
channelsMessages = {}
channelList = []
users = []


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
        
        if request.form.get("username") in users:
            return apology("Name already exists", 403)

        session["user_id"] = request.form.get("username")
        users.append(request.form.get("username"))

        return redirect("/")

    else:
        return render_template("getName.html")

@app.route("/logout")
def logout():
    try :
        users.remove(session["user_id"])
    except:
        pass
    session.clear()

    return redirect("/")
        
@app.route('/create', methods=["POST"])
@name_required
def create():
    if request.form.get("groupName"):
        channelList.append(request.form.get("groupName"))
    return redirect("/")

@app.route('/channels',methods=["GET", "POST"])
@name_required
def enterChannel():

    currentChannel = request.form.get("group")
    if currentChannel in channelList:
        return render_template("index.html", channels= channelList, messages=channelsMessages[currentChannel])
    else:
        return redirect("/")






