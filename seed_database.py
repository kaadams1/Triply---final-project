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

# Create movies, store them in list so we can use them
# to create fake ratings
activities_in_db = []
for activity in activity_data:
    activity_name = (
        activity["activity_name"],
    )
    # release_date = datetime.strptime(movie["release_date"], "%Y-%m-%d")

    db_activity = model.Activity.create(activity_name)
    activities_in_db.append(db_activity)

model.db.session.add_all(activities_in_db)
model.db.session.commit()

# Create 10 users; each user will make 10 ratings
for n in range(10):
    email = f"user{n}@test.com"
    password = "test"

    user = model.User.create(email, password)
    model.db.session.add(user)

    # for _ in range(10):
    #     random_movie = choice(movies_in_db)
    #     score = randint(1, 5)

    #     rating = model.Rating.create(user, random_movie, score)
    #     model.db.session.add(rating)

model.db.session.commit()