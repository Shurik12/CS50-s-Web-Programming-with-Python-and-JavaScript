from store_variables import *
from flask import render_template, redirect, request
from collections import deque
from flask_socketio import SocketIO, emit, join_room, leave_room

@app.route("/create", methods=["GET", "POST"])
def create_channel():
    """ Create a channel and redirect to its page """

    # Get channel name from form
    newChannel = request.form.get("channel")

    if request.method == "POST":
        if newChannel in channelsCreated:
            return render_template("error.html", message="that channel already exists!")
        # Add channel to global list of channels
        channelsCreated.append(newChannel)

        # Add channel to global dict of channels with messages
        # Every channel is a deque to use popleft() method 
        # https://stackoverflow.com/questions/1024847/add-new-keys-to-a-dictionary
        channelsMessages[newChannel] = deque()

        return redirect("/channels/" + newChannel)
    else:
        return render_template("create.html", channels = channelsCreated)

@socketio.on("joined", namespace='/')
def joined():
    """ Send message to announce that user has entered the channel """
    # Save current channel to join room.
    room = session.get('current_channel')
    join_room(room)
    emit('status', {
        'userJoined': session.get('username'),
        'channel': room,
        'msg': session.get('username') + ' has entered the channel'}, 
        room=room)