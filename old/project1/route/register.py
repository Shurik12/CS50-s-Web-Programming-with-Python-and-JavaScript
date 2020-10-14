from flask import Blueprint, session, render_template, redirect, request, flash
from route.db import db

reg_api = Blueprint('reg_api', __name__)

@reg_api.route("/register", methods=["GET", "POST"])
def register():
    """ Register user """
    
    # Forget any user_id
    session.clear()

    if request.method == "POST":

        # get variables from form
        username, password, confirm = request.form.get("username"), request.form.get("password"), request.form.get("confirmation")

        # check username
        if not username: return render_template("error.html", message = "Enter username")
        
        if db.execute("SELECT count(*) FROM users WHERE username = '%s'" % username).fetchone()[0] != 0: 
            return render_template("error.html", message="username already exist")

        # check password
        if not password: return render_template("error.html", message = "Enter password")

        # Ensure confirmation wass submitted 
        if not confirm: return render_template("error.html", message="must confirm password")

        # Check passwords are equal
        elif not password == confirm: return render_template("error.html", message="passwords didn't match")

        # Insert register into DB
        db.execute("INSERT INTO users (username, password) VALUES ('%s', '%s')" % (username, password))

        # Commit changes to database
        db.commit()

        # popup message
        flash('New account created', 'info')

        # Redirect user to login page
        return redirect("/login")

    else: return render_template("register.html")