import os

from flask import Flask, session, render_template, redirect
from flask_session import Session

from route.search import search_api
from route.register import reg_api
from route.login import login_api
from route.book import book_api
from route.search_api import my_api
from route.db import db
from route.login_required import login_required

def create_app():
	app = Flask(__name__)
	app.register_blueprint(reg_api)
	app.register_blueprint(login_api)
	app.register_blueprint(search_api)
	app.register_blueprint(book_api)
	app.register_blueprint(my_api)

	# Configure session to use filesystem
	app.config["SESSION_PERMANENT"] = False
	app.config["SESSION_TYPE"] = "filesystem"
	return app

app = create_app()
Session(app)

@app.route("/")
#@login_required
def index():
    return render_template("index.html")

@app.route("/logout")
def logout():
    """ Log user out """
    # Forget any user ID
    session.clear()
    # Redirect user to login form
    return redirect("/")

if __name__ == "__main__":
	app.run()
