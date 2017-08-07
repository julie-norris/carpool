"""Models and database functions for carpool."""

from flask_sqlalchemy import flask_sqlalchemy

db = SQLAlchemy()

class People(db.Model):
    """Creates Users and stores pertinent information."""

    __tablename__ = "people"

    user_id = db.Column(db.Integer, 
                        autoincrement=True,
                        primary_key=True)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(64), nullable=False)
    fname = db.Column(db.String(15), nullable=False)
    lname = db.Column(db.String(15), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    license_number = db.Column(db.String(20), nullable=False)

    #### Define Relationships ###



class Address(db.Model):
    """ Stores all addresses """

    __tablename__ = "addresses"

    add_id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True)
    street_address = db.Column(db.String(64), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    state = db.Column(db.String(15), nullable=False)
    zip_code = db.Column(db.String(15), nullable=False)
    latitude = db.Column(db.String(20), nullable=True)
    longitude = db.Column(db.String(20), nullable=True)
    name_of_place = db.Column(db.String(200), nullable=True)



class Driving_Route(db.Model):
    """Routes being driven by drivers with seats available."""

    __tablename__ = "driving_routes"

    route_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    start_add_id = db.Column(db.Integer,
                             db.ForeignKey('addresses.add_id'))
    end_add_id = db.Column(db.Integer, 
                           db.ForeignKey('addresses.add_id'))
    arrival_time = db.Column(db.Integer, nullable=False)###Will be a pulldown menu with time increments"""
    driver_id = db.Column(db.Integer,
                          db.ForeignKey('people.user_id'))
    num_seats = db.Column(db.Integer, nullable=False)#### Limited range - 1-6###

    
    ####define relationships###
    starting_address = db.relationship('Address', backref='driving_routes')
    end_address = db.relationship('Address', backref='driving_routes')
    driver = db.relationship('People', backref='driving_routes')





class User_Address(db.Model):
    """Addresses linked to a specific user."""

    __tablename__ = "user_addresses"

    user_address_id = db.Column(db.Integer,
                                autoincrement=True,
                                primary_key=True)
    add_id = db.Column(db.Integer,
                       db.ForeignKey('addresses.add_id'))
    user_id = db.Column(db.Integer,
                        db.ForeignKey('people.user_id'))

    ###define relationships###
    addressId = db.relationship('Address', backref='user-addresses')
    userId = db.relationship('People', backref='user-addresses')



class Ride(db.Model):
    """Middle Table for Users and Routes"""

    __tablename__ = "rides"


    rider_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    route_id = db.Column(db.Integer,
                         db.ForeignKey('driving_routes.route_id'))
    rider_id = db.Column(db.Integer,
                         db.ForeignKey('people.user_id'))

    ####define relationships####
    routeId = db.relationship('Route', backref='rides')
    riderId = db.relationship('People', backref='rides')


class Ride_Need(db.Model):
    """Rider Events"""

    __tablename__ = "ride_needs"

    ride_needs_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    start_address_id = db.Column(db.Integer,
                           dbForeignKey('addresses.add_id'))
    end_address_id = db.Column(db.Integer,
                           dbForeignKey('addresses.add_id'))
    arrival_time = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('people.user_id'))
    seats_needed = db.Column(db.Integer, 
                             ForeignKey('driving_routes.num_seats'))


    ###Define Relationships####
    user = db.relationship("People", backref='ride_needs')
    adress = db.relationship('Address', backref='ride_needs')
    seats = db.relationship('Driving_Route', backref='ride_needs')
    start = db.relationship('Address', backref='ride_needs')
    end = db.relationship('Address', backref='ride_needs')


# class Event_Routes(db.Model):
#     """Middle Table for Events and Routes"""

#     __tablename__ = "Event-Routes"

#     _id = db.Column(db.Integer,
#                    autoincrement=True,
#                    primary_key=True)
#     event_id = db.Column(db.ForeignKey('ride-needed.event_id'))
#     route_id = db.Column(db.ForeignKey('driving-routes.route_id'))

    #####define relationships####
    # eventId = db.relationship('Event', backref='event-routes')
    # routeId = db.relationship('Routes', backref='event-routes')



    ##########################################################################
    #Helper Functions

    def connect_to_db(app):

        app.config['SQLALCHEMY_DATABASE_URI'] ### WHAT GOES HERE?###
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        db.app = app
        db.init_app(app)

    if __name__ == "__main__":

        from server import app
        connect_to_db(app)


