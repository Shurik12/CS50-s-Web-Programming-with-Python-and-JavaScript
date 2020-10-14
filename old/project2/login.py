from flask import session, render_template, redirect, request
from flask_socketio import SocketIO, emit
from store_variables import *

@app.route("/login", methods=["GET", "POST"])
def login():
    ''' Save the username on a Flask session 
    after the user submit the sign in form '''

    # Forget any username
    session.clear()
    username = request.form.get("username")
    if request.method == "POST":
        if len(username) < 1 or username is '':
            return render_template("error.html", message="username can't be empty.")
        if username in usersLogged:
            return render_template("error.html", message="that username already exists!")                   
        usersLogged.append(username) # добавляем юзера в юзерлог
        session['username'] = username
        # Remember the user session on a cookie if the browser is closed.
        session.permanent = True
        return redirect("/")
    else: return render_template("login.html")

