""" CarPool"""

from jinja2 import StrictUndefined

from flask import Flask, request, jsonify, render_template, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import db, People, Address, Driving_Route, User_Address, Ride, Ride_Need
app = Flask(__name__)

app.secret_key = "SOMETHINGDIFFERENT"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage"""

    return render_template("homepage.html")


@app.route('/register', methods=['GET'])
def registration():
    """Shows registration page. Users input personal profile info."""

    return render_template("registration.html")

@app.route('/register', methods=['POST'])
def add_new_user():
    """Creates a new user in the database."""

    email = request.form["email"]
    password = request.form["password"]
    fname = request.form["first_name"]
    lname = request.form["last_name"]
    phone = request.form["phone_number"]
    license_number = request.form["license_number"]

    user = People.query.filter_by(email=email).first()

    if user:
        flash("You have already registered! Please log-in!")
        return redirect("/login")

    else:    
    user = People(email=email, password=password, fname=fname, lname=lname,
                  phone=phone_number, license_number=license_number)

    db.session.add(user)
    db.session.commit()

#  NEED SOMETHING HERE TO MAKE SURE THEY ARE LOGGED IN -- IS THIS ENOUGH:
    session["email"] = people.email 
    
    flash("Thank you for registering for CarPool! You have been logged in!")
    
    return redirect("/lets_go")


@app.route('/login')
def log_in():

    


@app.route('/logout')
def logout():



@app.route('/lets_go', methods=['POST'])
def create_profile():
    """Create a Route for a user."""



    

    
