from flask import session, render_template, redirect, request
from flask_socketio import SocketIO, emit
from store_variables import *
from login_required import login_required


@app.route("/channels/<channel>", methods=['GET','POST'])
@login_required
def enter_channel(channel):
    """ Show channel page to send and receive messages """

    # Updates user current channel
    session['current_channel'] = channel

    if request.method == "POST":
        
        return redirect("/")
    else:
        return render_template("channel.html", channels= channelsCreated, messages=channelsMessages[channel])

@socketio.on('send message')
def send_msg(msg, timestamp):
    """ Receive message with timestamp and broadcast on the channel """
    # Broadcast only to users on the same channel.
    room = session.get('current_channel')

    # Save 100 messages and pass them when a user joins a specific channel.

    if len(channelsMessages[room]) > 100:
        # Pop the oldest message
        channelsMessages[room].popleft()

    channelsMessages[room].append([timestamp, session.get('username'), msg])

    emit('announce message', {
        'user': session.get('username'),
        'timestamp': timestamp,
        'msg': msg}, 
        room=room)

