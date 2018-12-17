""" The backend for a Folf application. This is the 3rd project in the Python
course SC-T-308-PRLA at Reykjavik University Late-fall 2018."""

# TODO Remove unused dependencies... and clean up
from itertools import chain
from services.firebase import Firebase
from flask import Flask, render_template, request, redirect, url_for, flash, session, g
from services.forms import RegistrationForm, LoginForm, ResetForm, PlayGameForm


# Initializing the application.
app = Flask(__name__)


# Required for wtforms validation and session tracking.
app.config['SECRET_KEY'] = '5791628fb0b12ce0c676dfde280ba345'


# Initializing the database API service.
firebase = Firebase()


# Hard-coded global variables for the purpose of this prototype.
# For fixed Top Players at a location for this demo.
LOCATION = 'Reykjavík'
COURSE = 'Laugardalur'
MANY = 5


@app.before_request
def before_request():
    """ A wrapper function to check for the user ID. It runs before each call
    to route functions."""

    # Using the 'g' global object from Flask. Appending the user ID.
    g.uId = None
    if 'uId' in session:
        g.uId = session['uId']


@app.route('/')
def index():
    """ The landing page route. Methods: GET."""

    # For dynamic titles the title needs to be passed.
    return render_template('landing-page.html', title='Welcome')


@app.route("/home")
def home():
    """ The 'Home' page. It is the.... """

    # Here we're checking if the user is logged in.
    if g.uId:
        # If the user is verified we render the page.
        # Pass the user ID and sidebar data to be rendered.
        return render_template('home.html',
                               user=firebase.get_user_by_uId(g.uId),
                               topGames=firebase.get_top_players_at_course(
                                   LOCATION, COURSE, MANY),)
    else:
        # If the user verification fails, redirect to login page.
        return redirect(url_for('login'))


@app.route('/courses/<location>/<course>/<color>', methods=['GET', 'POST'])
def play_game(location, course, color):
    """ A route to render the play sheet page. It accepts three variables in
    the URI. With the 'location', 'course' and 'color' a dynamically rendered
    play sheet is served. Method: GET POST."""

    # Here we're checking if the user is logged in.
    if g.uId:
        # Initializing wtform validation object.
        form = PlayGameForm()
        # Get the relevant data from database API service.
        courseInfo = firebase.get_course_details(location, course, color)
        # Check the request method from client.
        if request.method == 'POST':
            # If the form passes all validation upon submition.
            if form.validate_on_submit():
                # This a data transfer object destined for the database.
                if firebase.add_game_to_user({
                    "uId": g.uId,
                    "location": location,
                    "course": course,
                    "color": color,
                    "game": [x.data for x in form][:10]
                }):
                    return redirect(url_for('courses'))
        # If the method was GET.
        # Pass the user ID and sidebar data to be rendered.
        return render_template('play-game.html',
                               user=firebase.get_user_by_uId(g.uId),
                               form=form, topGames=None, courseInfo=courseInfo)
    else:
        # If the user verification fails, redirect to login page.
        return redirect(url_for('login'))


@app.route("/courses")
def courses():
    """ Route to render all courses in the database. Method: GET."""

    # Here we're checking if the user is logged in.
    if g.uId:
        # Call to the database API services.
        course_dict = firebase.get_all_locations_and_courses()
        # Pass the user ID and sidebar data to be rendered.
        return render_template('courses.html',
                               user=firebase.get_user_by_uId(g.uId),
                               course_dict=course_dict,
                               topGames=firebase.get_top_players_at_course(
                                   LOCATION, COURSE, MANY))
    else:
        # If the user verification fails, redirect to login page.
        return redirect(url_for('login'))


@app.route("/games")
def games():
    """ Route that returns all the games logged by the user. Method: GET."""

    # Here we're checking if the user is logged in.
    if g.uId:
        # Call to the database API services for the game history.
        games = firebase.get_all_games_by_uId(g.uId)
        # Pass the user ID and sidebar data to be rendered.
        return render_template('games.html',
                               game_list=games,
                               user=firebase.get_user_by_uId(g.uId),
                               topGames=firebase.get_top_players_at_course(
                                   LOCATION, COURSE, MANY))
    else:
        # If the user verification fails, redirect to login page.
        return redirect(url_for('login'))


@app.route("/login", methods=['GET', 'POST'])
def login():
    """ Route that returns the login form for the site. Method: GET POST."""

    # Initializing wtform validation object.
    form = LoginForm()
    # Checking for request mothod.
    if request.method == 'POST':
        # If the form passes all validation upon submition.
        if form.validate_on_submit():
            # Call to database API services with user input.
            user = firebase.sign_in_user(
                email=form.email.data, password=form.password.data)
            # If user exists, he/she is logged in.
            if user is not False:
                flash('You have been logged in!', 'success')
                # Add the user ID to the session.
                session['uId'] = user['localId']
                # The user is redirected to the home page.
                return redirect(url_for('home'))
        # If the valdation fails the user is notified.
        flash('Login Unsuccessful. Please check username and password',
              'danger')
    # For GET requests the form is rendered and relevant data is passed.
    return render_template('login.html',
                           title='Login',
                           form=form,
                           user=firebase.get_user_by_uId(g.uId),
                           topGames=firebase.get_top_players_at_course(
                               LOCATION, COURSE, MANY))


@app.route("/register", methods=['GET', 'POST'])
def register():
    """ Route that returns the registration form for the site.
    Method: GET POST."""

    # Initializing wtform validation object.
    form = RegistrationForm()
    # Checking for request mothod.
    if request.method == 'POST':
        # If there is a user ID it is removed from the session.
        session.pop('uId', None)
        # If the form passes all validation upon submition.
        if form.validate_on_submit():
            # The user input is sent to the database.
            user = firebase.add_user({
                "name": form.name.data,
                "email": form.email.data,
                "password": form.email.data
            })
            # If the database was able to write the data.
            if user is not False:
                flash(f'Account created for {form.email.data}!', 'success')
                # Add the user ID to the session.
                session['uId'] = user['localId']
                # The user is redirected to the home page.
                return redirect(url_for('home'))
        # If the valdation fails the user is notified.
        flash(f'User email already exists: {form.email.data}!', 'danger')
    # For GET requests the form is rendered and relevant data is passed.
    return render_template('register.html',
                           title='Register',
                           form=form,
                           user=firebase.get_user_by_uId(g.uId),
                           topGames=firebase.get_top_players_at_course(
                               LOCATION, COURSE, MANY))


@app.route('/rules')
def rules():
    """ Route that returns the rules to be rendered. Method: GET."""

    rules = firebase.get_rules().split('"')
    result = []
    for rule in rules:
        if rule == '' or rule.startswith(','):
            continue
        result.append(rule)

    return render_template('rules.html',
                           rules=result,
                           user=firebase.get_user_by_uId(g.uId),
                           topGames=firebase.get_top_players_at_course(
                               LOCATION, COURSE, MANY))


@app.route('/logout')
def logout():
    """ Route to log off the user and close the session. Method: GET."""

    # The user ID is popped off the session.
    session.pop('uId', None)
    return redirect(url_for('login'))


@app.route('/reset', methods=['GET', 'POST'])
def reset():
    """ Route that lets the user reset the password via e-mail. Method: GET."""

    # Initializing wtform validation object.
    form = ResetForm()
    # Checking for request mothod.
    if request.method == 'POST':
        # If there is a user ID it is removed from the session.
        session.pop('uId', None)
        # If the form passes all validation upon submition.
        if form.validate_on_submit():
            # Check if the reset email was sent.
            if firebase.reset_password(form.email.data):
                flash(
                    f'Email sent to {form.email.data} for password reset!',
                    'success')
                return redirect(url_for('login'))
            # If the mail was not sent.
            flash(f'Email does not exists: {form.email.data}!', 'danger')
    # For GET requests the form is rendered and relevant data is passed.
    return render_template('reset.html',
                           title='Reset Password',
                           form=form, user=firebase.get_user_by_uId(g.uId),
                           topGames=firebase.get_top_players_at_course(
                               LOCATION, COURSE, MANY))


# Check if the file was imported. If not, enable the debugger and run the app.
if __name__ == '__main__':
    app.debug = True
    app.run()
