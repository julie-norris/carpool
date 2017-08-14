""" CarPool"""

from jinja2 import StrictUndefined

from flask import Flask, request, jsonify, render_template, flash, session, redirect
from flask_debugtoolbar import DebugToolbarExtension

from model import db, connect_to_db, Person, Address, Driving_Route, User_Address, Ride, Ride_Need
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

@app.route('/register_newperson', methods=['POST'])
def add_new_user():
    """Creates a new user in the database."""

    email = request.form["email"]
    password = request.form["password"]
    fname = request.form["first_name"]
    lname = request.form["last_name"]
    phone = request.form["phone_number"]
    license_number = request.form["license_number"]

    user = Person.query.filter_by(email=email).first()

    if user:
        flash("You have already registered! Please log-in!")
        return redirect("/login")

    else:    
        user = Person(email=email, password=password, fname=fname, lname=lname,
                  phone=phone_number, license_number=license_number)

    db.session.add(user)
    db.session.commit()

#  NEED SOMETHING HERE TO MAKE SURE THEY ARE LOGGED IN -- IS THIS ENOUGH:
    session["email"] = user.email 
    
    flash("Thank you for registering for CarPool! You have been logged in!")
    
    return redirect("/driver_or_rider")

@app.route('/login', methods=['GET'])
def show_login_form():

    return render_template("login.html")


@app.route('/login_process', methods=['POST'])
def login_process():

    email = request.form["email"]
    password = request.form["password"]

    user = Person.query.filter_by(email=email).first()

    if not user:
        flash("Log-in failed. Have you registered?")
        return redirect("/register")
    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")
    return redirect("/driver_or_rider")

@app.route('/driver_or_rider', methods=['GET'])
def is_user_driver_or_rider():

    return render_template("driving_or_riding.html")


@app.route('/driver', methods=['POST'])
def driver_letsgo():
    
    return render_template("Let's_go!.html")

@app.route('/map', methods=['POST'])
def driving_map():

    end_address=request.form.get("destination")
    start_address=request.form.get("start_address")
    


    return redirect('/rider')
    

@app.route('/rider', methods=['GET'])
def rider_mapwithroutes():

    return render_template("map_routes.html")

# @app.route('/lets_go')
# def create_profile():
#     """Create a Route for a user."""

#     return render_template("Let's_Go!.html")

# @app.route('/map_route') ## Need to pass in the variables from the Let's Go form)
# def showmap_and_availablerides():

###DISPLAY MAP WITH ALL THE POSSIBLE ROUTES SHOWN###

    return redirect('/confirmation')

@app.route('/confirmation')
def confirmsdriver_and_rider():
    pass

@app.route('/logout')
def logout():
    pass







if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)



    

    
