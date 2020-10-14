from flask import Blueprint, session, render_template, redirect, request
from route.db import db

login_api = Blueprint('login_api', __name__)

@login_api.route("/login", methods=["GET", "POST"])
def login():
    """ Log user in """

    # Forget any user_id
    session.clear()

    username, password = request.form.get("username"), request.form.get("password")

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not username: return render_template("error.html", message="must provide username")

        # Ensure password was submitted
        elif not password: return render_template("error.html", message="must provide password")

        # Query database for username (http://zetcode.com/db/sqlalchemy/rawsql/)
        # https://docs.sqlalchemy.org/en/latest/core/connections.html#sqlalchemy.engine.ResultProxy
        result = db.execute("SELECT id, username FROM users WHERE username = '%s' and password = '%s'" % (username, password)).fetchone()

        # Ensure username exists and password is correct
        if result == None: return render_template("error.html", message="invalid username and/or password")

        # Remember which user has logged in
        print (result)
        session["user_id"], session["user_name"] = result

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else: return render_template("login.html")
