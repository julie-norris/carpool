""" CarPool"""

from jinja2 import StrictUndefined

from flask import Flask, request, jsonify, render_template, flash, session
from flask import flask_debugger import DebugToolbarExtension

from model import connect_to_db, db, People, Address, Driving_Route, User_Address, Ride,
                    Ride_Need, 
app = Flask(__name__)

app.secret_key = "SOMETHINGDIFFERENT"

app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage"""

    return render_template("homepage.html")
