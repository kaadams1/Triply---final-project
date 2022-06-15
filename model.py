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

    # @classmethod
    # def create(cls, user_fname, user_lname, email, password):
    #    """Create and return a new user."""

    #    return cls(email=email, password=password)

    # @classmethod
    # def get_by_id(cls, user_id):
    #     return cls.query.get(user_id)

    # @classmethod
    # def get_by_email(cls, email):
    #     return cls.query.filter(User.email == email).first()

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
    #backref to scheduled activities

    def __repr__(self):
        return f"<Itinerary itin_id={self.itin_id} itin_name={self.itin_name}>"

    # @classmethod
    # def create(cls, itin_name, itin_location, itin_start, itin_end):
    #     """Create and return a new itinerary."""

    #     return cls(
    #         itin_name=itin_name,
    #         itin_location=itin_location,
    #         itin_start=itin_start,
    #         itin_end=itin_end,
    #         )


class Activity(db.Model):
    """An activity."""

    __tablename__ = "activities"

    activity_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    activity_name = db.Column(db.String(30), nullable=False, unique=False)
    city_id = db.Column(db.Integer, db.ForeignKey("cities.city_id"))
    activity_date = db.Column(db.Date, nullable=True, unique=False)
    activity_pic = db.Column(db.String)

    city = db.relationship("City", backref="activities")
    scheduledactivities = db.relationship("SchedActivity", backref="activity")

    # def connect_to_db(app, db_uri="postgresql:///testdb"):
    #     app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
    #     db.app = app
    #     db.init_app(app)

    # def example_data():
    #     """Create example data for the test database."""
    #     # write a function that creates a game and adds it to the database.
    #     Activity.query.delete()

    #     ex1 = Activity(activity_name='London Bridge')
    #     ex2 = Activity(activity_name='The Forbidden Forest')
    #     ex3 = Activity(activity_name='Sesame Street')

    #     db.session.add_all([ex1, ex2, ex3])
    #     db.session.commit()


    def __repr__(self):
        return f"<Activity activity_id={self.activity_id} activity_name={self.activity_name}>"



class SchedActivity(db.Model):
    """A scheduled activity."""

    __tablename__ = "scheduledactivities"

    sched_act_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    activity_id = db.Column(db.Integer, db.ForeignKey("activities.activity_id"))
    itin_id = db.Column(db.Integer, db.ForeignKey("itineraries.itin_id"))
    sched_act_date = db.Column(db.Date, nullable=True, unique=False)

    # activity = db.relationship("Activity", backref="scheduledactivities") - attribute for free
    itinerary = db.relationship("Itinerary", backref="scheduledactivities")

    def __repr__(self):
        return f"<Scheduled activity sched_act_id={self.sched_act_id} activity_id={self.activity_id} itin_id={self.itin_id}>"



class City(db.Model):
    """A city."""

    __tablename__ = "cities"

    city_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    city_name = db.Column(db.String(25), nullable=False, unique=False)
    country_name = db.Column(db.String(25), nullable=False, unique=False)

    # activities = db.relationship("Activity", backref="city") - attibute for free
    destinations = db.relationship("Destination", backref="city")

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

    def __repr__(self):
        return f"<Destination dest_id={self.dest_id} city_id={self.city_id} itin_id={self.itin_id}>"



def connect_to_db(flask_app, db_uri="postgresql:///activities", echo=True):
    flask_app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    flask_app.config["SQLALCHEMY_ECHO"] = echo
    flask_app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = flask_app
    db.init_app(flask_app)



if __name__ == "__main__":
    from server import app

    # Call connect_to_db(app, echo=False) if your program output gets
    # too annoying; this will tell SQLAlchemy not to print out every
    # query it executes.

    # connect_to_db(app)