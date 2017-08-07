"""Utility file to seed database"""

from sqlalchemy import func

from model import People, Address, Route, Driving_Route, User_Address, Ride, Ride_Need, 
                    connect_to_db, db

from server import app




def load_users():

    print "People"

    for i, row in enumerate(open('u.user')):
        row = row.rstrip()

        user_id, email, password, fname, lname, license = row.split(",")

        people = People(user_id=user_id, 
                        email=email,
                        password=password,
                        fname=fname,
                        lname=lname,
                        license=license)

        db.session.add(people)

    db.session.commit()

if __name__ == "__main__":
    connect_to_db(app)
    db.create_all()

    load_users()