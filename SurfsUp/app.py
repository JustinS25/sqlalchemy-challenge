# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################

app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route("/")
def home():
    """Available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )

# Precipitation Route

@app.route("/api/v1.0/precipitation")
def precipitation():

    """Return JSON representation of dictionary"""
    # Query precipitation results
    date_range = dt.date(2017,8,23) - dt.timedelta(days = 365)
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= date_range).all()

    session.close()

    # Create a dictionary from the row data and append prcp values
    prcp_list = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)
    
    return jsonify(prcp_list)

# Stations Route

@app.route("/api/v1.0/stations")
def stations():

    """Return JSON list of stations"""
    # Query precipitation results
    stations = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(stations))

    return jsonify(station_list)

# Tobs Route

@app.route("/api/v1.0/tobs")
def tobs():

    """Return JSON list of temperature observations"""
    # Query precipitation results
    date_range1 = dt.date(2017,8,23) - dt.timedelta(days = 365)
    active_station = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281',Measurement.date >= date_range1).all()

    session.close()

    # Convert list of tuples into normal list
    station_active_1 = list(np.ravel(active_station))

    return jsonify(station_active_1)

if __name__ == '__main__':
    app.run(debug=True)