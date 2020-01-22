""" CarPool"""

from jinja2 import StrictUndefined
import requests, pprint, json
from flask import Flask, request, jsonify, render_template, flash, session, redirect

from flask_debugtoolbar import DebugToolbarExtension
from model import db, connect_to_db, Person, Address, Driving_Route, User_Address, Ride, Ride_Need
import re
from datetime import datetime, time
from time import sleep
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse
import os


account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
twilio_number = os.environ['TWILIO_NUMBER']
client = Client(account_sid, auth_token)

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
    session['logged_in'] = True
    

    flash("Logged in")

    if driver_or_rider == 'driver':
        return redirect("/driver")
    else:
        return redirect("/rider")



@app.route('/driver', methods=['GET'])
# add @login_required...
def driver_letsgo():

    # if current_user.is_authenticated:
    return render_template("Let's_go!.html")
    # else:
    #     flash("Please log in!")
    #     return redirect ("/login")

@app.route('/map', methods=['POST'])
def driving_map():
    time_input = request.form.get('arrival_time')
    date_input = request.form.get('date')
    date_time = date_input + "|" + time_input
    
    
    start_address=request.form.get("originInput")
    payload = {'key': '####################', 'address': start_address}
    app.logger.info(start_address)
    app.logger.info(payload)
    try:
        info = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=payload, timeout=3.0)
    except requests.exceptions.ConnectionError as e:
        app.logger.error("Couldn't connect to google maps: {}".format(e.msg))
    
    end_address=request.form.get("destinationInput")
    payload_2 = {'key': '#################', 'address': end_address}
    info_2 = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=payload_2, timeout=3.0)


    arrival_time_date = datetime.strptime(date_time, '%Y-%m-%d|%H:%M')
    num_seats=int(request.form.get('num_seats'))


    start_address = extract_data_fordb(info)
    end_address = extract_data_fordb(info_2)
    
   
    create_drivingroute(start_address, end_address, arrival_time_date, num_seats)
    return redirect("/thank_you")

def extract_data_fordb(data):
    
    binary = data.content
    output = json.loads(binary)

    # app.logger.debug(json.dumps(output, indent=4))

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

@app.route('/match_ride_rider', methods=['GET'])
def rider():
    """Finds a ride for the rider and displays options"""

    # rider = session.get("user_id")
    destination = request.args.get("rider_destination1")
    payload = {'key': '########', 'address': destination}
    info = requests.get('https://maps.googleapis.com/maps/api/geocode/json', params=payload)
    binary = info.content
    output = json.loads(binary)
    
    # No longer needed; left here for future reference:
    # app.logger.debug(json.dumps(output, indent=4))
    

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
    print street_address
    address = Address.query.filter_by(street_address=street_address, 
                                      city=city, 
                                      state=state, 
                                      zip_code=zip_code).first()
    if street_address == address.street_address:
        destination = address.add_id

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

        destination = address.add_id
    
  

    destination = address.add_id
    time_input = request.args.get('time')
    date_input = request.args.get('date')
    date_time = date_input + "|" + time_input
    arrival_time_date = datetime.strptime(date_time, '%Y-%m-%d|%H:%M')
    seats_needed = int(request.args.get("num_seats"))
 
  # see if the destination address of rider is already in the addresses database; then 
  # get the add_id and match it to the end_add_id from the Driving Route

    sql = """SELECT * 
    FROM driving_routes AS dr
    WHERE dr.end_add_id = :dest_needed
    AND dr.arrival_time_date <= :time_needed
    AND CAST(dr.arrival_time_date AS DATE) = :date_input
    AND :seats_needed <= dr.num_seats - (SELECT COUNT(*)
                                        FROM rides as r
                                        WHERE r.route_id = dr.route_id)"""

    available_routes = db.session.execute(sql, {"dest_needed": destination,
                                                "time_needed": arrival_time_date,
                                                "seats_needed": seats_needed,
                                                "date_input": date_input}).fetchall()
    available_routes = [Driving_Route.query.get(available_route[0]) for available_route in available_routes]
    
    # data = {'available_routes':available_routes}
    # return jsonify(data)
    return render_template('ride_links.html', routes=available_routes)
    
# Here I need to take the routes that were identified as matches and display them
# on the rider's map page. I think this is where I need AJAX


@app.route('/get_ride/<int:route_id>', methods=['POST'])
def create_ridetaken(route_id):

    rider = request.form.get('user_id')

    ride = Ride(route_id=route_id,
                rider=rider)

    db.session.add(ride)
    db.session.commit()
# put the ride in the session to use in the confirmation page
    session["ride"] = (ride.route_id, ride.rider)
    return redirect("/confirmation")
# # @app.route('/map_route') ## Need to pass in the variables from the Let's Go form)
# # def showmap_and_availablerides():

# ###DISPLAY MAP WITH ALL THE POSSIBLE ROUTES SHOWN###

@app.route('/thank_you')
def thanks():
   
   return render_template('thank_you.html')

@app.route('/confirmation')
def confirmsdriver_and_rider():
# get the ride from the session
    ride = session.get("ride")
# query the session 'ride' to get the route_id which can be used to get the driver
# object
    driving_route = Driving_Route.query.get(ride[0])
    driver = driving_route.user
# get the person object that matches the rider; ride[1] = the index of the rider in the
# session 'ride'
    rider = Person.query.get(ride[1]) 
    

    return render_template('confirmation.html', driver=driver, 
                                                ride=ride,
                                                rider=rider)
@app.route('/sms', methods=['POST'])
def sms():
    driver_number = request.form.get('d_number')
    num = '+1' + driver_number
    rider_number = request.form.get('r_number')
    
    message_body = "Please confirm details with the rider @" + rider_number
    try:
        new_message = client.messages.create(to=num,
                                        from_=twilio_number,
                                        body=message_body)
        return redirect('/logout')
    except:

        return redirect('/logout')

@app.route('/logout')
def ask_logout():
   
   return render_template('logout.html')


@app.route('/logout', methods=['POST'])
def logout():
    
    yes_no = request.form.get('yesno')

    if yes_no == 'yes':

        del session["user_id"]
        flash("Logged out.")
        return redirect("/")

    elif yes_no == 'no_driver':

        return render_template("Let's_Go!.html")
    else:
        return render_template("map_routes.html")




if __name__ == "__main__":
    connect_to_db(app)
    app.run(host="0.0.0.0", debug=True)



    

    
