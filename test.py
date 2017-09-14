from flask import Flask, session
from model import db, Person, Address, Driving_Route, User_Address, Ride, Ride_Need, connect_to_db, example_data
from seed import example_data
from server import app
import unittest 


class FlaskTestsDatabase(unittest.TestCase):
    """Flask tests that use the database"""

    def setUp(self):
        """Stuff to do before every test."""
        # Get the Flask test client
        self.client = app.test_client()
        app.config['TESTING'] = True
        
        # Connect to test database 
        connect_to_db(app, "postgresql:///testdb")

        # Create tables and add sample data
        db.create_all()
        example_data()

    def tearDown(self):
        """Do at end of every test."""

        db.session.close()
        db.drop_all()

    def test_login(self):
        """database test"""

        result = self.client.post("/login_process",
                                data={
                                "email": "happy@gmail.com", 
                                "password": "onefineday",
                                "typeofuser" : "driver"}, follow_redirects=True)

        self.assertIn("Logged in", result.data)

        # import pdb
        # pdb.set_trace()




if __name__ == '__main__':
    # If called like a script, run our tests
    unittest.main()

