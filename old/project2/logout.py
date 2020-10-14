from flask import session, redirect
from flask_socketio import SocketIO, send, emit, join_room, leave_room
from store_variables import *

@app.route("/logout", methods=["GET"])
def logout():
    try:
        usersLogged.remove(session['username'])
    except ValueError:
        pass
    # Delete cookie
    session.clear()

    return redirect("/")

@socketio.on("left", namespace='/')
def left():
    """ Send message to announce that user has left the channel """

    room = session.get('current_channel')

    leave_room(room)

    emit('status', {
        'msg': session.get('username') + ' has left the channel'}, 
        room=room)
