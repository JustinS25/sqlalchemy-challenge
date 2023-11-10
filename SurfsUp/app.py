# Import the dependencies.
import datetime as dt
import numpy as np
import pandas as pd

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from datetime import datetime

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
        f"--------------<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end<br/><br/>"
        f"Note: Start/End Date must be entered in following format:<br/>"
        f"YYYY-MM-DD<br/>"
    )

# Precipitation Route

@app.route("/api/v1.0/precipitation")
def precipitation():

    """Return JSON representation of dictionary"""
    # Query precipitation results
    date_range = dt.date(2017,8,23) - dt.timedelta(days = 365)
    results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= date_range).all()

    # Close session
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
    # Query station results
    stations = session.query(Station.station).all()

    # Close session
    session.close()

    # Convert list of tuples into normal list
    station_list = list(np.ravel(stations))

    return jsonify(station_list)

# Tobs Route

@app.route("/api/v1.0/tobs")
def tobs():

    """Return JSON list of temperature observations for most active station"""
    # Query date/tobs results
    date_range1 = dt.date(2017,8,23) - dt.timedelta(days = 365)
    active_station = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == 'USC00519281',Measurement.date >= date_range1).all()

    # Close session
    session.close()

    # Convert list of tuples into normal list
    station_active_1 = list(np.ravel(active_station))

    return jsonify(station_active_1)

# Start and Start/End

@app.route("/api/v1.0/<start_date>")
def start_day(start_date):
    """Return JSON list of min temp, avg temp, and max temp for range of dates"""

    # If an end date is not set, we use all dates after the start date
    # Convert start date to date type
    start_date = datetime.strptime(start_date,'%Y-%m-%d')
    # start_date = dt.date(2017,5,23)
    # Perform a query to retrieve the min, max, and average data
    # Filter start_date <= date_range
    func_results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date).all()

    # Close session
    session.close()

    # Convert list of tuples into normal list
    func_results_1 = list(np.ravel(func_results))

    return jsonify(func_results_1)


@app.route("/api/v1.0/<start_date>/<end_date>")
def start_end(start_date,end_date):
    """Return JSON list of min temp, avg temp, and max temp for range of dates"""

    # Convert start and end dates to date type
    start_date = datetime.strptime(start_date,'%Y-%m-%d')
    end_date = datetime.strptime(end_date,'%Y-%m-%d')

    # Perform a query to retrieve the min, max, and average data
    # Filter start_date <= date_range <=end_date
    func_results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start_date,Measurement.date <= end_date).all()

    # Close session
    session.close()

    # Convert list of tuples into normal list
    func_results_1 = list(np.ravel(func_results))

    return jsonify(func_results_1)

if __name__ == '__main__':
    app.run(debug=True)