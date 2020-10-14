from store_variables import *
from create_channel import *
from enter_channel import *
from login import *
from logout import *
from login_required import login_required
from flask import session, render_template
from flask_ngrok import run_with_ngrok

@app.route("/")
@login_required
def index():
    print (session['username'], 1)
    return render_template("index.html", channels=channelsCreated)

if __name__ == '__main__':
    socketio.run(app, host = "0.0.0.0", port = "4326", debug = False)


