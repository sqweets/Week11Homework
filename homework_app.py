#################################################
# Dependencies
#################################################
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

#################################################
# Flask Setup
#################################################
homework_app = Flask(__name__)

#################################################
# Database Setup
#################################################

# Create Database Connection
engine = create_engine('sqlite:///Resources/hawaii.sqlite')

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Routes
#################################################

@homework_app.route("/")
def welcome():
    # List all available api routes.
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;start&gt;/&lt;end&gt;<br/>"
    )


@homework_app.route("/api/v1.0/precipitation")
# Query for the dates and temperature observations from the last year.
# Convert the query results to a Dictionary using `date` as the key and `tobs` as the value.
# Return the JSON representation of your dictionary.
def precipitation():
    query_results = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= "2016-08-23").filter(Measurement.date <= "2017-08-23").all()

    precip_dict = {}
    # Convert to dictionary
    for entry in query_results:
        precip_dict[entry[0]] = entry[1]

    return jsonify(precip_dict)


@homework_app.route("/api/v1.0/stations")
# Return a JSON list of stations from the dataset.
def stations():
    query_results = session.query(Station.station, Station.name).all()

    station_dict = {}
    # Convert to dictionary
    for entry in query_results:
        station_dict[entry[0]] = entry[1]

    return jsonify(station_dict)


@homework_app.route("/api/v1.0/tobs")
# Return a JSON list of Temperature Observations (tobs) for the previous year.
def tobs():
    query_results = session.query(Measurement.date, Measurement.tobs).\
    filter(Measurement.date >= "2016-08-23").filter(Measurement.date <= "2017-08-23").all()

    temp_dict = {}
    # Convert to dictionary
    for entry in query_results:
        temp_dict[entry[0]] = entry[1]

    return jsonify(temp_dict)


@homework_app.route("/api/v1.0/<start>")
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
def summary_from_date(start):
    comp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()

    start_dict = {}
    # Convert to dictionary
    start_dict['min'] = comp_results[0][0]
    start_dict['avg'] = comp_results[0][1]
    start_dict['max'] = comp_results[0][2]

    return jsonify(start_dict)


@homework_app.route("/api/v1.0/<start>/<end>")
# Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range.
# When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
def summary_date_range(start, end):
    comp_results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).filter(Measurement.date <= end).all()

    range_dict = {}
    # Convert to dictionary
    range_dict['min'] = comp_results[0][0]
    range_dict['avg'] = comp_results[0][1]
    range_dict['max'] = comp_results[0][2]

    return jsonify(range_dict)


if __name__ == '__main__':
    homework_app.run(debug=True)