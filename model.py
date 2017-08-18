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
    arrival_time_date_date = db.Column(db.Time, nullable=False)###Store in UTC. Will be a pulldown menu with time increments"""
    driver_id = db.Column(db.Integer,
                          db.ForeignKey('people.user_id'))
    num_seats = db.Column(db.Integer, nullable=False)#### Limited range - 1-6###

    
    driver = db.relationship('Person', backref='driving_routes')





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
    arrival_time_date = db.Column(db.Time, nullable=False)
    user_id = db.Column(db.Integer,
                        db.ForeignKey('people.user_id'))
    seats_needed = db.Column(db.Integer, 
                             nullable=False)


    ###Define Relationships####
    user = db.relationship("Person", backref='ride_needs')
    # start = db.relationship('Address', backref='ride_needs')
    # end = db.relationship('Address', backref='ride_needs')



    ##########################################################################
    #Helper Functions
def example_data():
    """Sample Data to Test Database"""

    usr1 = Person(email='happy@gmail.com', password='onefineday', fname='Smiley', lname='Dwarf',
                    phone='425-222-2222', license_number='Null')
    usr2 = Person(email='grumpy@gmail.com', password='onceuponatime', fname='Grump', lname='Dwarf',
                    phone='425-222-2223', license_number='Null')
    usr3 = Person(email='sneezey@gmail.com', password='tissueplease', fname='Snee', lname='Zeee',
                    phone='425-222-2224', license_number='Null')

    Address1 = Address(street_address='321 Main Street', city='Alameda', state='CA', zip_code='94501',
                    latitude = 'Null', longitude='Null', name_of_place='Alameda Point Gym')
    Address2 = Address(street_address='425 Webster', city='Alameda', state='CA', zip_code='94501',
                    latitude ='Null', longitude='Null', name_of_place='Alameda Karate')
    Address3 = Address(street_address='2 Hornet Drive', city='Alameda', state='CA', zip_code='94501',
                    latitude='Null', longitude='Null', name_of_place='Hornet Field')
    Address4 = Address(street_address='1 Boulder Canyon Road', city='Boulder', state='CO', zip_code='80303',
                    latitude='Null', longitude='Null', name_of_place='CU Boulder')

    db.session.add_all([usr1,usr2,usr3,Address1,Address2,Address3,Address4])
    db.session.commit()

def connect_to_db(app, database_uri='postgresql:///carpool'):

    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":

    from server import app
    connect_to_db(app)

    db.create_all()



