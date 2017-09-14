"""Models and database functions for carpool."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Person(db.Model):
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

    
    @property
    def serialize(self):
        "returns data in easibly jsonifiable format"
        return {
            "user_id": self.user_id,
            "email": self.email,
            "name": "{} {}".format(self.fname, self.lname),
            "phone": self.phone,
            "license_number": self.license_number
        }

class Address(db.Model):
    """ Stores all addresses """

    __tablename__ = "addresses"

    add_id = db.Column(db.Integer,
                       autoincrement=True,
                       primary_key=True)
    street_address = db.Column(db.String(64), nullable=False)
    city = db.Column(db.String(64), nullable=False)
    state = db.Column(db.String(15), nullable=True)
    zip_code = db.Column(db.String(15), nullable=True)
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
    arrival_time_date = db.Column(db.DateTime, nullable=False)###Store in UTC. Will be a pulldown menu with time increments"""
    driver_id = db.Column(db.Integer,
                          db.ForeignKey('people.user_id'))
    num_seats = db.Column(db.Integer, nullable=False)#### Limited range - 1-6###

    
    user = db.relationship('Person', backref='driving_routes')
    start_address = db.relationship('Address', foreign_keys=[start_add_id])
    end_address = db.relationship('Address', foreign_keys=[end_add_id])


    @property
    def serialize(self):
        "returns data in easibly jsonifiable format"
        return {
            "route_id": self.route_id,
            "start_add_id": self.start_add_id,
            "end_add_id": self.end_add_id,
            "arrival_time_date": self.arrival_time_date,
            "driver_id": self.driver_id,
            "num_seats": self.num_seats
        }



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
    userId = db.relationship('Person', backref='user-addresses')



class Ride(db.Model):
    """Middle Table for Users and Routes"""

    __tablename__ = "rides"

    rider_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    route_id = db.Column(db.Integer,
                         db.ForeignKey('driving_routes.route_id'))
    rider = db.Column(db.Integer,
                         db.ForeignKey('people.user_id'))

    ####define relationships####
    route = db.relationship('Driving_Route', backref='rides')
    person_riding = db.relationship('Person', backref='rides')


class Ride_Need(db.Model):
    """Rider Events"""

    __tablename__ = "ride_needs"

    ride_needs_id = db.Column(db.Integer,
                         autoincrement=True,
                         primary_key=True)
    start_address_id = db.Column(db.Integer,
                           db.ForeignKey('addresses.add_id'))
    end_address_id = db.Column(db.Integer,
                           db.ForeignKey('addresses.add_id'))
    arrival_time_date = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('people.user_id'))
    seats_needed = db.Column(db.Integer, 
                             nullable=False)


    ###Define Relationships####
    user = db.relationship("Person", backref='ride_needs')
    
    @property
    def serialize(self):
        "returns data in easibly jsonifiable format"
        return {
            "user_id": self.people.user_id,
            "email": self.people.email,
            "name": "{} {}".format(self.people.fname, self.people.lname),
            "phone": self.people.phone
        }




    ##########################################################################
    #Helper Functions
def connect_to_db(app, database_uri='postgresql:///carpool'):

    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    from server import app
    connect_to_db(app)

    db.create_all()



