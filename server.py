"""Server for trip itinerary app."""
from pprint import pformat
import os
import requests
from flask import Flask, render_template, request, flash, session, redirect
from forms import RegistrationForm, GreetUserForm, SearchActivities, NewItinerary
from model import connect_to_db, db, User, Activity, SchedActivity, City, Destination, Itinerary
from jinja2 import StrictUndefined
import pandas as pd
from datetime import datetime

app = Flask(__name__)
app.secret_key = "noguessinggames4653"
app.jinja_env.undefined = StrictUndefined

API_KEY = os.environ['YELP_KEY']




@app.route("/", methods=["GET", "POST"])
def homepage():
    """View homepage."""

    form = RegistrationForm()

    return render_template("homepage.html", form=form)

#USERS

@app.route("/users", methods=["GET", "POST"])
def register_user():
    """Create a new user."""

    form = RegistrationForm()

    if request.method == "POST":
        
        if form.validate_on_submit():

            user_fname = request.form.get("first_name")
            user_lname = request.form.get("last_name")
            email = request.form.get("email")
            password = request.form.get("password")
            
            user = User.get_by_email(email)

            if user:
                flash("Email already in use. Try again.")

            else:
                user = User.create(user_fname, user_lname, email, password)
                db.session.add(user)
                db.session.commit()
                flash("Account created! Please log in.")

                # if user in session:
                #     session["user"] = user

        else:
            if form.password.errors:
                for error in form.password.errors:
                    flash(error)
            # return form.errors

    return redirect("/")



@app.route("/users/my-profile")
def my_profile():
    """Show details on a particular user."""

    if "user_email" in session:
        user = User.get_by_email(session["user_email"])
    else:
        flash("Please log in!")
        return redirect("/")

    return render_template("user-details.html", user=user)


@app.route("/login", methods=["POST"])
def process_login():
    """Process user login."""

    form = GreetUserForm()

    email = request.form.get("email")
    password = request.form.get("password")

    user = User.get_by_email(email)

    if not user or user.password != password:
        flash("The email or password you entered was incorrect.")
        return redirect('/')

    else:
        # Log in user by storing the user's email in session
        session["user_email"] = user.email
        user = User.get_by_email(session["user_email"])

        return render_template("user-details.html", user=user)


@app.route('/logout')
def logout():
    session.pop('user_email', None)
    return redirect('/')


#ITINERARIES

@app.route("/new-itinerary", methods=["GET"])
def display_new_itin_form():
    """Display a form to create new itinerary. Goes with def create_new_itin()."""

    form = NewItinerary()

    return render_template("new-itinerary.html", form=form)


@app.route("/new-itinerary", methods=["POST"])
def create_new_itin():
    """Create a new itinerary."""

    form = NewItinerary()

    # if request.method == "POST":
        
    #     if form.validate_on_submit():

    itin_name = request.form.get("itin_name")
    itin_location = request.form.get("itin_location")
    city_name = request.form.get("itin_location")
    itin_start= request.form.get("itin_start")
    itin_end = request.form.get("itin_end")

    email = session["user_email"]
    user = User.get_by_email(email)
    trip = Itinerary.check_for_trip(user.user_id, itin_location, itin_start)

    if trip:
        flash("This itinerary already exists!")
        return render_template("new-itinerary.html")

    else:
        trip = Itinerary.create(user.user_id, itin_name, itin_location, itin_start, itin_end)
        db.session.add(trip)
        db.session.commit()

        trip = Itinerary.check_for_trip(user.user_id, itin_location, itin_start)

        city = City.get_by_name(city_name)

        if not city:
            city = City.create(city_name=city_name)

            db.session.add(city)
            db.session.commit()

            city = City.get_by_name(city_name)

        destination = Destination.create(city_id=city.city_id, itin_id=trip.itin_id)
        db.session.add(destination)
        db.session.commit()

                # destination = Destination.get_by_itin_id(trip.itin_id)

        return redirect(f"/display-itinerary/{trip.itin_id}")

        # else:
        #     for error in form.errors:
        #         flash(error)

    # else:
    #     return redirect('/new-itinerary')
    

@app.route("/display-new-itinerary/<itin_id>")
def display_new_itinerary(itin_id):
    """Display the newly created itinerary."""
    trip = Itinerary.get_by_id(itin_id)

    return render_template("display-new-itinerary.html", trip=trip)


@app.route("/view-itineraries", methods=["GET"])
def view_itineraries():
    """View a list of itineraries created by the user."""

    email = session["user_email"]
    user = User.get_by_email(email)

    itin_list = Itinerary.return_itineraries(user.user_id)

    for itin in itin_list:
        itin.itin_start = itin.itin_start.strftime('%m-%d-%Y')
        itin.itin_end = itin.itin_end.strftime('%m-%d-%Y')

    return render_template("view-itineraries.html", itin_list=itin_list)


@app.route("/display-itinerary/<itin_id>")
def display_itinerary(itin_id):
    """Display a single itinerary from the user's list."""

    trip = Itinerary.get_by_id(itin_id)
    form = NewItinerary()

    unscheduled_activities = [s.activity for s in trip.scheduledactivities if not s.sched_act_date]

    scheduled_activities = SchedActivity.query.filter(SchedActivity.itin_id==itin_id, SchedActivity.sched_act_date!=None).all()

    trip.itin_start = trip.itin_start.strftime('%m-%d-%Y')
    trip.itin_end = trip.itin_end.strftime('%m-%d-%Y')
    
    itin_dates = pd.date_range(start=trip.itin_start, end=trip.itin_end)
    itin_dates2 = []
    
    for d in itin_dates:
        # conv_date = date.strftime('%m-%d-%Y')
        itin_dates2.append(d.date())

    return render_template("display-itinerary.html", trip=trip, form=form, unscheduled_activities=unscheduled_activities, 
                                scheduled_activities=scheduled_activities, itin_dates2=itin_dates2)


@app.route("/edit-itinerary/<itin_id>", methods=["GET"])
def edit_details(itin_id):
    """Edit main details of a chosen itinerary."""
    trip = Itinerary.get_by_id(itin_id)

    return render_template("edit-itinerary.html", trip=trip)
    
    
@app.route("/edit-itinerary-fields", methods=["POST"])
def edit_itinerary_fields():
    """Enter and save new details of a chosen itinerary."""
    
    itin_id = request.json["itin_id"]

    updated_name = request.json.get("updated_name", None)
    updated_location = request.json.get("updated_location", None)
    updated_start = request.json.get("updated_start", None)
    updated_end = request.json.get("updated_end", None)

    Itinerary.update(itin_id, updated_name, updated_location, updated_start, updated_end)
    db.session.commit()    
    
    return "Success! Field updated."



#ACTIVITIES

@app.route("/search/<itin_id>", methods=["GET"])
def search_activities(itin_id):
    """Search activities by city or zip."""

    trip = Itinerary.get_by_id(itin_id)
    form = SearchActivities()
    location = request.args.get('search_location')

    return render_template("search.html", trip=trip, form=form, location=location)


@app.route("/search-results/<itin_id>", methods=["GET"])
def list_searched_activities(itin_id):
    """List activities from search."""

    trip = Itinerary.get_by_id(itin_id)
    
    location = request.args.get('search_location')

    url = 'https://api.yelp.com/v3/businesses/search'
    payload = { 'location' : location,
                'radius' : 40000,
                'term' : 'attractions' }

    header = { 'Authorization' : f"Bearer {os.environ['YELP_KEY']}" }

    response = requests.get(url, params=payload, headers=header)
        
    json_response = response.json() 

    return render_template('search-results.html', 
                            trip=trip, location=location,
                            pformat=pformat,
                            json_response=json_response)


@app.route('/activity/<id>')
def get_activity_details(id):
    """View the details of an activity."""

    url = f'https://api.yelp.com/v3/businesses/search/{id}'
    payload = {'apikey': YELP_KEY}

    response = requests.get(url, params=payload)
    activity = response.json()

    return render_template('activity-details.html',
                           activity=activity,
                           activities=activities)


@app.route("/add-activity", methods=["GET"])
def add_activity():
    """Add activity to the database."""

    itin_id = request.args.get("itin-id")
    activity_name = request.args.get("activity-name")
    destination = Destination.get_by_itin_id(itin_id)
    city_id = destination.city_id
    trip = Itinerary.get_by_id(itin_id)

    activity = Activity.create(activity_name=activity_name, city_id=city_id)

    trip.activities.append(activity)

    db.session.add(trip)
    db.session.commit()

    return redirect(f"/display-itinerary/{trip.itin_id}")


@app.route("/list-chosen-activities", methods = ["GET"])
def list_chosen_activities():
    """List chosen activities on display-itinerary page, where they can be scheduled 
        by the user and converted to scheduled activities."""

    itin_id = request.args.get("itin-id")
    trip = Itinerary.get_by_id(itin_id)

    return redirect(f"/display-itinerary/{trip.itin_id}")


@app.route("/schedule-activity/<itin_id>/<activity_id>", methods = ["POST"])
def schedule_activity(itin_id, activity_id):
    """Schedule an activity from the activities list, moving to scheduled activities."""

    trip = Itinerary.get_by_id(itin_id)

    sched_act_date = request.form.get('date')

    #get sched activity by activity ID and itin ID
    sched_activity = SchedActivity.get_by_trip_id_act_id(itin_id, activity_id)
    #if sched activity:
    if sched_activity:
        sched_activity.sched_act_date=sched_act_date
        #modify/add date
    else:
        scheduledactivity = SchedActivity.create(activity_id, itin_id, sched_act_date)
    #instead of creating, check to see if in database
    #if it is, update the date; if not, create

        trip.scheduledactivities.append(scheduledactivity)
        db.session.add(scheduledactivity)
    
    db.session.commit()

    return redirect(f"/display-itinerary/{trip.itin_id}")


@app.route("/list-scheduled-activities", methods = ["GET"])
def list_scheduled_activity():
    """List scheduled activities on the display-itinerary page."""

    itin_id = request.args.get("itin-id")
    trip = Itinerary.get_by_id(itin_id)

    activities = trip.activities
    scheduledactivities = trip.scheduledactivities

    return redirect(f"/display-itinerary/{trip.itin_id}")



if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)