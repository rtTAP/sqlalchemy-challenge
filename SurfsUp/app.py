# Import the dependencies.
import numpy as np
import os
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################

# Create engine using the `hawaii.sqlite` database file
engine = create_engine("sqlite:///SurfsUp/Resources/hawaii.sqlite")

# Declare a Base using `automap_base()`
Base = automap_base()

# Use the Base class to reflect the database tables
Base.prepare(autoload_with=engine)

# Assign the measurement class to a variable called `Measurement` and
# the station class to a variable called `Station`
Measurement = Base.classes.measurement
Station = Base.classes.station


# Create a session
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
#Part2.
#Q1 start homepage and list all available routes
@app.route("/")
def home():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation"
        f"/api/v1.0/stations"
        f"/api/v1.0/tobs"
        f"/api/v1.0/<start>"
        f"/api/v1.0/<start>/<end>"
    )

#Q2 precipitation routes with date as the key
@app.route("/api/v1.0/precipitation")
def precipitation():
#Query for the dates and precipitation values
    results = session.query(Measurement.date, Measurement.prcp).all()

#Convert to list of dictionaries to jsonify
    precipitation_data = []
    for date, prcp in results:
        data = {}
        data["date"] = date
        data["prcp"] = prcp
        precipitation_data.append(data)

    return jsonify(precipitation_data)

#Q3 station routes 
@app.route("/api/v1.0/stations")
def stations():
#Query for the station data
    results = session.query(Station.station).all()

#Convert to list to jsonify
    stations = list(np.ravel(results))

    return jsonify(stations)

#Q4 temperature observations for the most active station for the last year of data
@app.route("/api/v1.0/tobs")

def tobs():
    station_id = 'USC00519281'

    one_year_ago = dt.date(2017, 8, 23) - dt.timedelta(days=365)

    latest_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]

#Query for the temperature observation data
    results = session.query(Measurement.date, Measurement.tobs) \
    .filter(Measurement.station == station_id) \
    .filter(Measurement.date >= one_year_ago) \
    .filter(Measurement.date <= latest_date) \
    .all()

#Convert list to jsonify
    tobs_data = list(np.ravel(results))

    return jsonify(tobs_data)

#Q5 start and end date range routes
@app.route("/api/v1.0/<start>")
def start(start):
#Query for the minimum temperature, the average temperature, and the maximum temperature for a specified start
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

#Convert to list to jsonify
    start_data = list(np.ravel(results))

    return jsonify(start_data)

@app.route("/api/v1.0/<start>/<end>")
def start_end(start, end):
#Query for the minimum temperature, the average temperature, and the maximum temperature for a specified start-end range
    results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

#Convert to list to jsonify
    start_end_data = list(np.ravel(results))

    return jsonify(start_end_data)

if __name__ == '__main__':
    app.run(debug=True)