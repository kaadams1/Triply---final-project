"""Script to seed database."""

import os
import json
from random import choice, randint
from datetime import datetime

import model
import server

os.system("dropdb activities")
os.system("createdb activities")

model.connect_to_db(server.app)
model.db.create_all()

# Load movie data from JSON file
with open("data/yelp.json") as f:
    activity_data = json.loads(f.read())

activities_in_db = []
for activity in activity_data:
    activity_name = (activity["activity_name"])

    db_activity = model.Activity.create(activity_name)
    activities_in_db.append(db_activity)

model.db.session.add_all(activities_in_db)
model.db.session.commit()

# Create 10 users
for n in range(10):
    email = f"user{n}@test.com"
    password = "test"
    user_fname = "User"
    user_lname = "Test"

    user = model.User.create(email, password, user_fname, user_lname)
    model.db.session.add(user)

model.db.session.commit()