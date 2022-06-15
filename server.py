"""Server for trip itinerary app."""
from pprint import pformat
import os
import requests
from flask import Flask, render_template, request, flash, session, redirect

# from model import connect_to_db, db, User, Activity, SchedActivity, City, Destination, Itinerary

from jinja2 import StrictUndefined

app = Flask(__name__)
app.secret_key = "noguessinggames4653"
app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ['YELP_KEY']


@app.route("/")
def homepage():
    """View homepage."""

    return render_template("homepage.html")


@app.route("/users", methods=["POST"])
def register_user():
    """Create a new user."""

    user_fname = request.form.get("first_name")
    user_lname = request.form.get("last_name")
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.get_by_email(email)

    if user:
        flash("Cannot create an account with that email. Try again.")

    else:
        user = User.create(email, password)
        db.session.add(user)
        db.session.commit()
        flash("Account created! Please log in.")

    return redirect("/")


@app.route("/users/<user_id>")
def show_user(user_id):
    """Show details on a particular user."""

    user = User.get_by_id(user_id)

    return render_template("user_details.html", user=user)


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.get_by_email(email)
    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        flash(f"Welcome back, {user.email}!")

    return redirect("/")


@app.route("/search", methods=["GET"])
def search_activities():
    """Search nearby attractions."""

    location = request.args.get('location', '')
    radius = request.args.get('radius', '20000')
    term = requests.args.get('term', 'attractions')

    url = 'https://api.yelp.com/v3/businesses/search'
    payload = { 'apikey' : API_KEY,
                'location' : location,
                'radius' : radius,
                'term' : term }

    response = requests.get(url, params=payload)
    data = response.json()

    if '_embedded' in data:
        activities = data['_embedded']['activities']
    else:
        activities = []

    return render_template('search-results.html',
                            pformat=pformat,
                            data=data,
                            activities=activities)



if __name__ == "__main__":
    # connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)