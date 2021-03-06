from flask import Flask, render_template, Response, jsonify, request, session
from flask_session import Session
from sql_utils import *
from tempfile import mkdtemp
from camera import VideoCamera
import cv2

from helpers import login_required

app = Flask(__name__)

video_stream = VideoCamera()

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route('/', methods=["GET", "POST"])
def index():

    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return render_template("apology.html", error="Must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("apology.html", error="Must provide password")

        # Ensure confirmation password was submitted
        elif not request.form.get("password"):
            return render_template("apology.html", error="Must provide confirmation of password")

        # Ensure username is unique by querying database for username
        username = request.form.get("username")
        query = 'SELECT * FROM users WHERE user_name = ?'
        params = (username,)
        result = sqliteExecute(query, params)
        print(result)

        password1 = request.form.get("password")
        password2 = request.form.get("confirm password")

        if len(rows) != 0:
            return render_template("apology.html", error="Username has already been taken, please choose a new one")

        # Ensure password and confirmed password match
        elif (password1 != password2):
            return render_template("apology.html", error="Passwords do not match")

        elif len(password1) < 6 and any(map(str.isdigit, password1)) == False:
            return render_template("apology.html", error="Password requires at least 6 characters and must include a number")

        # input user into database
        query = 'INSERT INTO users (username, hash) VALUES (?, ?)'
        params = (request.form.get("username"), generate_password_hash(password1))
        result = sqliteExecute(query)
        #db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=request.form.get("username"), hash=generate_password_hash(password1))
        return redirect("/")

    else:
        return render_template("register.html")


@app.route('/scan',  methods=["GET", "POST"])
@login_required
def scan():
    if request.method == 'POST':
        video_stream.save_frame()
    
    return render_template('scan.html')

def gen(camera):
    while True:
        frame = camera.get_frame()

        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')


@app.route('/video_feed', methods=["GET", "POST"])
def video_feed():
    return Response(gen(video_stream),
                mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True,port="5000")