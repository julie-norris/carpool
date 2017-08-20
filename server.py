""" CarPool"""

from jinja2 import StrictUndefined
import requests, pprint, json
from flask import Flask, request, jsonify, render_template, flash, session, redirect
from flask_debugtoolbar import DebugToolbarExtension
from model import db, connect_to_db, Person, Address, Driving_Route, User_Address, Ride, Ride_Need
import re
from datetime import datetime, time



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

    driver_or_rider = request.form["typeofuser"]
    email = request.form["email"]
    password = request.form["password"]
    fname = request.form["fname"]
    lname = request.form["lname"]
    phone = request.form["phone_number"]
    license_number = request.form["license_number"]

    match = re.match(r'^[a-zA-Z0-9 -]{5,9}$', license_number)

    if not match:
        flash("Invalid license number. Try again.")
        return redirect("/register")

    user = Person.query.filter_by(email=email).first()

    if user:
        flash("You have already registered! Please log-in!")
        return redirect("/login")

    else:    
        user = Person(
            email=email,
            password=password,
            fname=fname,
            lname=lname,
            phone=phone, 
            license_number=license_number
            )

    db.session.add(user)
    db.session.commit()

#  NEED SOMETHING HERE TO MAKE SURE THEY ARE LOGGED IN -- IS THIS ENOUGH:
    session["user_id"] = user.user_id 
    
    flash("Thank you for registering for CarPool! You have been logged in!")
    
    if driver_or_rider == 'driver':
        return redirect("/driver")
    else:
        return redirect("/rider")

@app.route('/login', methods=['GET'])
def show_login_form():

    return render_template("login.html")


@app.route('/login_process', methods=['POST'])
def login_process():

    email = request.form["email"]
    password = request.form["password"]
    driver_or_rider = request.form["typeofuser"]

    user = Person.query.filter_by(email=email).first()

    if not user:
        flash("Log-in failed. Have you registered?")
        return redirect("/register")
    if user.password != password:
        flash("Incorrect password")
        return redirect("/login")

    session["user_id"] = user.user_id

    flash("Logged in")

    if driver_or_rider == 'driver':
        return redirect("/driver")
    else:
        return redirect("/rider")



@app.route('/driver', methods=['GET'])
def driver_letsgo():
    
    return render_template("Let's_go!.html")

@app.route('/map', methods=['POST'])
def driving_map():
    time_input = request.form.get('arrival_time')
    date_input = request.form.get('date')
    date_time = date_input + "|" + time_input
    
    print datetime.strptime(date_time, '%Y-%m-%d|%H:%M')
    
    start_address=request.form.get("originInput")
    payload = {'key': 'AIzaSyA5tDzhP-TkpUOI4dOZzkATen2OUCPasf4', 'address': start_address}
    info = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=payload)
    
    end_address=request.form.get("destinationInput")
    payload_2 = {'key': 'AIzaSyA5tDzhP-TkpUOI4dOZzkATen2OUCPasf4', 'address': end_address}
    info_2 = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=payload_2)

    # time_input = request.form.get('arrival_time')
    arrival_time_date = datetime.strptime(date_time, '%Y-%m-%d|%H:%M')
    num_seats=int(request.form.get('num_seats'))


    start_address = extract_data_fordb(info)
    end_address = extract_data_fordb(info_2)
    
   
    create_drivingroute(start_address, end_address, arrival_time_date, num_seats)
    return redirect("/thank_you")

def extract_data_fordb(data):
    
    binary = data.content
    output = json.loads(binary)

    app.logger.debug(json.dumps(output, indent=4))

    results = output['results'][0]
    latitude = results['geometry']['location']['lat']
    longitude = results['geometry']['location']['lng']
    street_number = None
    street_name = None
    city = None
    state = None
    zip_code = None

    for address_components in results['address_components']:
        
        if address_components['types'][0]=='street_number':
            street_number=address_components['short_name']
        if address_components['types'][0]=='route':
            street_name=address_components['short_name']
        if address_components['types'][0]=='locality':
            city=address_components['short_name']
        if address_components['types'][0]=="administrative_area_level_1":
            state=address_components['short_name']
        if address_components['types'][0]=="postal_code":
            zip_code=address_components['short_name']

    street_address = "{num} {name}".format(num=street_number, name=street_name)

    address = Address.query.filter_by(street_address=street_address, 
                                      city=city, 
                                      state=state, 
                                      zip_code=zip_code).first()
    if not address:
        address = Address(street_address=street_address, 
                          city=city,
                          state=state,
                          zip_code=zip_code,
                          latitude=latitude,
                          longitude=longitude,
                          name_of_place=None)
    
    
        db.session.add(address)
        db.session.commit()
    return address



def create_drivingroute(start_address,
                        end_address, 
                        arrival_time_date, 
                        num_seats):

    driver_id=session.get("user_id")
    
    start_add_id = start_address.add_id
    end_add_id = end_address.add_id

    driving_route = Driving_Route(
        driver_id=driver_id,
        start_add_id=start_add_id,
        end_add_id=end_add_id,
        arrival_time_date=arrival_time_date,
        num_seats=num_seats)

    db.session.add(driving_route)
    db.session.commit()

    return driving_route




@app.route('/rider', methods=['GET'])
def rider_mapwithroutes():

    return render_template("map_routes.html")

@app.route('/match_ride_rider', methods=['POST'])
def ride(num_seats):
    time_input = request.form.get('arrival_time')
    date_input = request.form.get('date')
    date_time = date_input + "|" + time_input
    arrival_time_date = datetime.strptime(date_time, '%Y-%m-%d|%H:%M')
    
    user_id = session.get("user_id")
    # route_id = Driving_Route.query.filter_by('route_id' where user_id = user_id)
#     # rides = Ride(route_id)







# # @app.route('/map_route') ## Need to pass in the variables from the Let's Go form)
# # def showmap_and_availablerides():

# ###DISPLAY MAP WITH ALL THE POSSIBLE ROUTES SHOWN###

#     return redirect('/confirmation')


@app.route('/thank_you')
def thanks():
   
   return render_template('thank_you.html')

@app.route('/confirmation')
def confirmsdriver_and_rider():
    pass

@app.route('/logout')
def logout():
    pass







if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)



    

    
