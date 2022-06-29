from datetime import datetime
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()



class User(db.Model):
    """A user."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_fname = db.Column(db.String(20), nullable=False, unique=False)
    user_lname = db.Column(db.String(20), nullable=False, unique=False)
    email = db.Column(db.String, unique=True)
    password = db.Column(db.String)

    #itineraries to user backref, itineraries attribute for free on User

    def __repr__(self):
        return f"<User user_id={self.user_id} email={self.email}>"

    @classmethod
    def create(cls, user_fname, user_lname, email, password):
       """Create and return a new user."""

       return cls(user_fname=user_fname, user_lname=user_lname, email=email, password=password)

    @classmethod
    def get_by_id(cls, user_id):
        return cls.query.get(user_id)

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter(User.email == email).first()

    # @classmethod
    # def all_users(cls):
    #     return cls.query.all()


class Itinerary(db.Model):
    """A trip."""

    __tablename__ = "itineraries"

    itin_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.user_id"))
    itin_name = db.Column(db.String(30), nullable=False, unique=False)
    itin_location = db.Column(db.String(30), nullable=False, unique=False)
    itin_start = db.Column(db.Date, nullable=False, unique=False)
    itin_end = db.Column(db.Date, nullable=False, unique=False)

    user = db.relationship("User", backref="itineraries")    
    destinations = db.relationship("Destination", backref="itinerary") #many to one
    #backref to scheduled activities - attribute for free
    activities = db.relationship("Activity", secondary="scheduledactivities", backref="itineraries")

    @classmethod
    def create(cls, user_id, itin_name, itin_location, itin_start, itin_end):
       """Create and return a new itinerary."""
       return cls(user_id=user_id, itin_name=itin_name, itin_location=itin_location, itin_start=itin_start, itin_end=itin_end)

    @classmethod
    def check_for_trip(cls, user_id=User.user_id, itin_location=itin_location, itin_start=itin_start):
        """Check to see if user has already created this trip. Returns boolean."""
        check_trip = Itinerary.query.filter_by(user_id=User.user_id, itin_location=itin_location, itin_start=itin_start).first()
        return check_trip

    @classmethod
    def return_itineraries(cls, user_id=User.user_id, itin_name=itin_name, itin_location=itin_location, itin_start=itin_start, itin_end=itin_end):
        """Return a list of all itineraries by the same user."""
        get_itins = Itinerary.query.filter_by(user_id=User.user_id).all()
        return get_itins

    @classmethod
    def get_by_id(cls, itin_id):
        """Return and view a single itinerary."""
        grab_itin = Itinerary.query.get(itin_id)
        return grab_itin

    @classmethod
    def update(cls, itin_id, updated_name = None, updated_location = None, updated_start = None, updated_end = None):
       """Update and return a new itinerary."""
       trip = cls.query.get(itin_id)

       if updated_name:
            trip.itin_name = updated_name
       if updated_location:
            trip.itin_location = updated_location
       if updated_start:
            trip.itin_start = updated_start
       if updated_end:
            trip.itin_end = updated_end


    def __repr__(self):
        return f"<Itinerary itin_id={self.itin_id} itin_name={self.itin_name}>"



class Activity(db.Model):
    """An activity."""

    __tablename__ = "activities"

    activity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    activity_name = db.Column(db.String, nullable=False, unique=False)
    city_id = db.Column(db.Integer, db.ForeignKey("cities.city_id"))

    city = db.relationship("City", backref="activities")
    scheduledactivities = db.relationship("SchedActivity", backref="activity")
    #secondary relationship to itinerary via backref

    @classmethod
    def create(cls, activity_name, city_id):
       """Create and return a new activity."""
       return cls(activity_name=activity_name, city_id=city_id)

    @classmethod
    def get_by_id(cls, activity_id):
        """Return and view a single activity."""
        grab_activity = Activity.query.get(activity_id)
        return grab_activity

    @classmethod
    def get_unsched_activities_by_itin(cls, itin_id):
        """Return unscheduled activities by itinerary."""
        grab_unsched_activities = Activity.query.filter_by(itin_id=itin_id).all()
        return grab_unsched_activities


    def __repr__(self):
        return f"<Activity activity_id={self.activity_id} activity_name={self.activity_name}>"



class SchedActivity(db.Model):
    """A scheduled activity."""

    __tablename__ = "scheduledactivities"

    sched_act_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey("activities.activity_id"))
    itin_id = db.Column(db.Integer, db.ForeignKey("itineraries.itin_id"))
    sched_act_date = db.Column(db.DateTime, nullable=True, unique=False)

    # activity = db.relationship("Activity", backref="scheduledactivities") - attribute for free
    itinerary = db.relationship("Itinerary", backref="scheduledactivities")

    @classmethod
    def create(cls, activity_id, itin_id, sched_act_date):
       """Create and return a new scheduled activity."""
       return cls(activity_id=activity_id, itin_id=itin_id, sched_act_date=sched_act_date)

    @classmethod
    def get_by_id(cls, sched_act_id):
        """Return and view a single scheduled activity."""
        grab_sched_act = SchedActivity.query.get(sched_act_id)
        return grab_sched_act

    @classmethod
    def get_by_trip_id_act_id(cls, itin_id, activity_id):
        get_by_trip_act = SchedActivity.query.filter_by(itin_id=itin_id, activity_id=activity_id).first()
        return get_by_trip_act

    # @classmethod
    # def get_sched_act_for_trip

    def __repr__(self):
        return f"<Scheduled activity sched_act_id={self.sched_act_id} activity_id={self.activity_id} itin_id={self.itin_id} sched_act_date={self.sched_act_date}>"



class City(db.Model):
    """A city."""

    __tablename__ = "cities"

    city_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    city_name = db.Column(db.String(25), nullable=False, unique=False)
    # country_name = db.Column(db.String(25), nullable=False, unique=False)

    # activities = db.relationship("Activity", backref="city") - attibute for free
    destinations = db.relationship("Destination", backref="city")

    @classmethod
    def create(cls, city_name):
       """Create and add city to the database."""
       return cls(city_name=city_name)

    @classmethod
    def get_by_id(cls, city_id):
        """Return and view a single city object."""
        grab_city_by_id = City.query.get(city_id)
        return grab_city_by_id

    @classmethod
    def get_by_name(cls, city_name):
        grab_city_by_name = City.query.filter_by(city_name=city_name).first()
        return grab_city_by_name


    def __repr__(self):
        return f"<City city_id={self.city_id} city_name={self.city_name}>"



class Destination(db.Model):
    """A destination."""

    __tablename__ = "destinations"

    dest_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey("cities.city_id"))
    itin_id = db.Column(db.Integer, db.ForeignKey("itineraries.itin_id"))

    # city = db.relationship("City", backref="destinations") - attribute for free
    # itinerary = db.relationship("Itinerary", backref="destinations") - attribute for free

    @classmethod
    def create(cls, city_id, itin_id):
        """Create a destination object to put in the database."""
        return cls(city_id=city_id, itin_id=itin_id)

    @classmethod
    def get_by_id(cls, dest_id):
        """Retrieve destination object using dest_id."""
        grab_dest_by_id = Destination.query.get(dest_id)
        return grab_dest_by_id

    @classmethod
    def get_by_itin_id(cls, itin_id):
        """Retrieve destination object using itin_id."""
        grab_dest_by_itin_id = Destination.query.filter_by(itin_id=itin_id).first()
        return grab_dest_by_itin_id

    @classmethod
    def get_by_city_id(cls, city_id):
        """Retrieve destination object using city_id."""
        grab_dest_by_city_id = Destination.query.filter_by(city_id=city_id).first()
        return grab_dest_by_city_id

    def __repr__(self):
        return f"<Destination dest_id={self.dest_id} city_id={self.city_id} itin_id={self.itin_id}>"



def connect_to_db(flask_app, db_uri="postgresql:///activities", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)

    print("Connected to the db!")


if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    connect_to_db(app)
    db.create_all()