from flask import Flask, render_template, Response, jsonify, request, session, redirect, flash
from flask_session import Session
import string
from sql_utils import *
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from tempfile import mkdtemp
from camera import VideoCamera
import cv2
from youtube_utils import youtube_search, get_video_codes, get_related_questions
from random import randint

from helpers import login_required

from predict import Predict

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
            #return render_template("apology.html", error="Must provide username", error_code=401)
            flash("Must provide username")
            return render_template("login.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            #return render_template("apology.html", error="Must provide password", error_code=401)
            flash("Must provide password")
            return render_template("login.html")

        # Query database for username
        username = request.form.get("username")
        query = 'SELECT * FROM Users WHERE user_name = ?'
        params = (username,)
        result = sqliteExecute(query, params)
     
        # Ensure username exists and password is correct
        if len(result) != 1 or not check_password_hash(result[0][2], request.form.get("password")):
            #return render_template("apology.html", error="Invalid username and/or password", error_code=401)
            flash("Incorrect username and/or password")
            return render_template("login.html")

        # Remember which user has logged in
        session["user_id"] = result[0][0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
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
            #return render_template("apology.html", error="Must provide username", error_code=400)
            flash("Must provide username")
            return render_template("register.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            #return render_template("apology.html", error="Must provide password", error_code=400)
            flash("Must provide password")
            return render_template("register.html")

        # Ensure confirmation password was submitted
        elif not request.form.get("password"):
            #return render_template("apology.html", error="Must provide confirmation of password", error_code=400)
            flash("Must provide confirmation of password")
            return render_template("register.html")

        # Ensure username is unique by querying database for username
        username = request.form.get("username")
        query = 'SELECT * FROM Users WHERE user_name = ?'
        params = (username,)
        result = sqliteExecute(query, params)
        #print(result)

        password1 = request.form.get("password")
        password2 = request.form.get("confirm password")

        if len(result) != 0:
            #return render_template("apology.html", error="Username has already been taken, please choose a new one", error_code=400)
            flash("Username has already been taken, please choose a new one")
            return render_template("register.html")

        # Ensure password and confirmed password match
        elif (password1 != password2):
            #return render_template("apology.html", error="Passwords do not match", error_code=400)
            flash("Passwords do not match")
            return render_template("register.html")

        elif len(password1) < 6 and any(map(str.isdigit, password1)) == False:
            #return render_template("apology.html", error="Password requires at least 6 characters and must include a number", error_code=400)
            flash("Password requires at least 6 characters and must include a number")
            return render_template("register.html")

        # input user into database
        query = 'INSERT INTO Users (user_name, hash) VALUES (?, ?)'
        params = (username, generate_password_hash(password1))
        result = sqliteExecute(query, params)
        #db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash)", username=request.form.get("username"), hash=generate_password_hash(password1))
        return redirect("/")

    else:
        return render_template("register.html")

@app.route('/featured',  methods=["GET", "POST"])
@login_required
def featured():
    # populate a list with tuples containing question_id and question_name
    random_questions = []
    i = 0
    counter = 0

    query = 'SELECT DISTINCT question_id FROM Questions'
    result = sqliteExecute(query)
    print(result)
    print(result.sort())

    while i < 10 and counter < 10:
        # pick question randomly
        q_id = randint(139, 258)
        query = 'SELECT * FROM Questions WHERE question_id = ?'
        params = (q_id,)
        result = sqliteExecute(query, params)

        if len(result) != 0:
            name = result[0][-1]
            if (q_id, name) not in random_questions:
                random_questions.append((q_id, name))
                i += 1

        counter += 1
    #print(questions)

    return render_template('featured.html', random_questions=random_questions)

@app.route('/scan',  methods=["GET", "POST"])
@login_required
def scan():
    if request.method == 'POST':
        # get scanned image from user
        img_name = video_stream.save_frame()
        image_path = "/Users/naresh/Documents/University/Hackathons/CUES_Global_Solutions_Hacakathon/lent21/static/images/" + img_name
        
        # render loading screen
        #render_template('scan.html', loading=1, feed=0, img_name=img_name)

        # predict what topic question is from
        Pred = Predict()
        search_key = Pred.predict(image_path) # get topic (search_key)

        # handle errors
        if search_key == "error":
            flash('Image was not scanned correctly, please try again!')
            return redirect('/scan')

        # search youtube for relevant videos
        results = youtube_search(search_key, max_results=3)
        vid_list = get_video_codes(results)
        print(vid_list)

        # find related videos
        related_questions = get_related_questions(search_key)

        # render final template
        return render_template('scan.html', loading=0, feed=0, img_name=img_name, search_key=search_key, vid_list=vid_list, related_questions=related_questions)
  
    return render_template('scan.html', loading=0, feed=1, related_questions=[])


def gen(camera):
    while True:
        frame = camera.get_frame()

        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/maths/<level>/<topics>')
@login_required
def maths(level, topics):

    if level == 'home' and topics == 'home':
        return render_template('maths.html', depth=0)
    elif topics == 'home':
        topics = get_topics_from_subject('Maths', level)
        return render_template('maths.html', depth=1, level=level, topics=topics)
    else:
        questions = get_questions_from_topic(level, topics)
        return render_template('maths.html', depth=2, level=level, topics=topics, questions=questions)

    

@app.route('/biology')
@login_required
def biology():
    return render_template('biology.html')

@app.route('/chemistry')
@login_required
def chemistry():
    return render_template('chemistry.html')

@app.route('/physics')
@login_required
def physics():
    return render_template('physics.html')

@app.route('/mental_health')
@login_required
def mental_health():
    return render_template('mental_health.html')

@app.route('/questions/<question_id>')
@login_required
def questions(question_id):
    # get question from question_id
    query = 'SELECT * FROM Questions WHERE question_id = ?'
    params = (question_id,)
    result = sqliteExecute(query, params)

    if len(result) == 0:
        return render_template("apology.html", error="No questions with that question id")

    # get related questions
    topics = result[0][3]
    related_questions = get_related_questions(topics)
    print(related_questions)
    
    # format strings for HTML
    level = result[0][1].upper()
    subject = result[0][2].capitalize()
    topics = topics.capitalize()
    question = result[0][-1].capitalize()

    return render_template('questions.html', level=level, subject=subject, topics=topics, question=question, related_questions=related_questions)


@app.route('/video_feed', methods=["GET", "POST"])
def video_feed():
    return Response(gen(video_stream),
                mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True,port="5000")