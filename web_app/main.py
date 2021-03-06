from flask import Flask, render_template, Response, jsonify, request, session, redirect
from flask_session import Session
from sql_utils import *
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from tempfile import mkdtemp
from camera import VideoCamera
import cv2
from youtube_utils import youtube_search, get_video_codes

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
            return render_template("apology.html", error="Must provide username")

        # Ensure password was submitted
        elif not request.form.get("password"):
            return render_template("apology.html", error="Must provide password")

        # Query database for username
        username = request.form.get("username")
        query = 'SELECT * FROM Users WHERE user_name = ?'
        params = (username,)
        result = sqliteExecute(query, params)
     
        # Ensure username exists and password is correct
        if len(result) != 1 or not check_password_hash(result[0][2], request.form.get("password")):
            return render_template("apology.html", error="Invalid username and/or password")

        # Remember which user has logged in
        session["user_id"] = result[0][0]

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
        query = 'SELECT * FROM Users WHERE user_name = ?'
        params = (username,)
        result = sqliteExecute(query, params)
        #print(result)

        password1 = request.form.get("password")
        password2 = request.form.get("confirm password")

        if len(result) != 0:
            return render_template("apology.html", error="Username has already been taken, please choose a new one")

        # Ensure password and confirmed password match
        elif (password1 != password2):
            return render_template("apology.html", error="Passwords do not match")

        elif len(password1) < 6 and any(map(str.isdigit, password1)) == False:
            return render_template("apology.html", error="Password requires at least 6 characters and must include a number")

        # input user into database
        query = 'INSERT INTO Users (user_name, hash) VALUES (?, ?)'
        params = (username, generate_password_hash(password1))
        result = sqliteExecute(query, params)
        #db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=request.form.get("username"), hash=generate_password_hash(password1))
        return redirect("/")

    else:
        return render_template("register.html")


@app.route('/scan',  methods=["GET", "POST"])
@login_required
def scan():
    if request.method == 'POST':
        img_name = video_stream.save_frame()
        results = youtube_search('indices', max_results=3)
        
        vid_list = get_video_codes(results)

        return render_template('scan.html', feed=0, img_name=img_name, vid_list=vid_list)


    
    return render_template('scan.html', feed=1)

@app.route('/maths')
def maths():
    return render_template('maths.html')

@app.route('/biology')
def biology():
    return render_template('biology.html')

@app.route('/chemistry')
def chemistry():
    return render_template('chemistry.html')

@app.route('/physics')
def physics():
    return render_template('physics.html')

@app.route('/mental_health')
def mental_health():
    return render_template('mental_health.html')

@app.route('/questions')
def mental_health():
    return render_template('question.html', related_questions=related_questions)

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