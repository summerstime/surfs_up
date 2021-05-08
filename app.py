# Import the dependencies
import datetime as dt
import pandas as pd
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

# Setup database engine
engine = create_engine("sqlite:///hawaii.sqlite")

# Reflect the database into our classes/tables
Base = automap_base()
Base.prepare(engine, reflect=True)

# Create variables for each class
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create a session line from Python to our database
session = Session(engine)

# Create a new Flask instance
app = Flask(__name__)

# Create the Welcome Route
@app.route('/')

# Create a function with a return statement
# f strings display the options to the user
def welcome():
    return(
        """Welcome to the Climate Analysis API!"""
        f"<br/><br/>Available Routes:<br/>"
        f"<br/>/api/v1.0/precipitation<br/>"
        f"<br/>/api/v1.0/stations<br/>"
        f"<br/>/api/v1.0/tobs<br/>"
        f"<br/>/api/v1.0/temp/start/end"
    )    

# Create the route for the precipitation function
@app.route("/api/v1.0/precipitation")
# Create the precipitation function
def precipitation():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    precipitation = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= prev_year).all()
    precip = {date: prcp for date, prcp in precipitation}
    return jsonify(precip)

# Create the route for the station function
@app.route("/api/v1.0/stations")
# Create the stations function
def stations():
    results = session.query(Station.station).all()
    stations = list(np.ravel(results))
    return jsonify(stations=stations)

# Create the route for the temperature observations function
@app.route("/api/v1.0/tobs")
# Create the temperature observations
def temp_monthly():
    prev_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    results = session.query(Measurement.tobs).\
        filter(Measurement.station == 'USC00519281').\
        filter(Measurement.date >= prev_year).all()
    temps = list(np.ravel(results))
    return jsonify(temps=temps)

# Create the starting and ending routes for min, avg, max temps
@app.route("/api/v1.0/temp/<start>")
@app.route("/api/v1.0/temp/<start>/<end>")
# Create a stats function for the start and end parameters
def stats(start=None, end=None):
    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    if not end:
        results = session.query(*sel).\
            filter(Measurement.date >= start).all()
        temps = list(np.ravel(results))
        return jsonify(temps=temps)

    results = session.query(*sel).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    temps = list(np.ravel(results))
    return jsonify(temps)



# Add ending to the list of commands
if __name__ == "__main__":
    print("example is being run directly.")
else:
    print("example is being imported")