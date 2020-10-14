import os

from flask import Flask, session
from flask_socketio import SocketIO, emit
from flask_ngrok import run_with_ngrok

app = Flask(__name__)
app.config["SECRET_KEY"] = "my key"
  # Start ngrok when app is run
socketio = SocketIO(app)


channelsCreated = []
channelsMessages = dict()
usersLogged = []
