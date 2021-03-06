############################################
# Import all dependencies
############################################
import numpy as np
import sqlalchemy
import pandas as pd
import datetime as dt

from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
from datetime import datetime, timedelta
from flask import url_for


############################################
#database
############################################
# create engine
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

############################################
# Setup Flask
############################################

app = Flask(__name__)

# Flask Routes
@app.route("/")
def home():
    return (
        f"<u><b><h1>The available routes below:</h1></u></b><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start_date<br/>"
        f"/api/v1.0/end_date<br/>"

    )

# Precipation data
@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    precip_query = session.query(measurement.date, measurement.prcp).all()
    session.close()

    # dictionary from the data
    hawaii_precip = []

    for date, prcp in precip_query:
        hawaii_prcp_dict = {}
        hawaii_prcp_dict["date"] = date
        hawaii_prcp_dict["prcp"] = prcp
        hawaii_precip.append(hawaii_prcp_dict)
    
    return jsonify(hawaii_precip)


# Station data
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations_query = session.query(station.station, station.name,
     station.latitude, station.longitude, station.elevation).all()
    session.close()

    # dictionary from the data
    hawaii_station = []

    for stations, names, latitude,longitude,elevation in stations_query:
        hawaii_station_dict = {}
        hawaii_station_dict["station"] = stations
        hawaii_station_dict["name"] = names
        hawaii_station_dict["latitude"] = latitude
        hawaii_station_dict["longitude"] = longitude
        hawaii_station_dict["elevation"] = elevation
        hawaii_station.append(hawaii_station_dict)
    
    return jsonify(hawaii_station)

# tobs data
@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)
    max_query = session.query(func.max(measurement.date)).one()
    max_date = max_query[0]
    max_date_conv = dt.datetime.strptime(max_date, '%Y-%m-%d')
    start_date = max_date_conv.date()

    days_in_year = dt.timedelta(365)
    end_date = start_date - days_in_year

    active_station_query = session.query(measurement.station, func.count(measurement.station))\
            .group_by(measurement.station).order_by(func.count(measurement.station).desc()).first()

    most_active_station = active_station_query[0]
    
    station_temp_query = session.query(measurement.station, measurement.date, measurement.tobs)\
                    .filter(measurement.station == most_active_station)\
                    .filter(measurement.date.between(end_date, start_date))


    session.close()

   # dictionary from the data
    hawaii_temps = []

    for station, date, tobs in station_temp_query:
        hawaii_tobs_dict = {}
        hawaii_tobs_dict["station"] = station
        hawaii_tobs_dict["date"] = date
        hawaii_tobs_dict["tobs"] = tobs
        hawaii_temps.append(hawaii_tobs_dict)
    
    return jsonify(hawaii_temps)

# start date data
@app.route("/api/v1.0/start_date")
def start_date():
##################
##working on it!##
##################
    session.close()


# end date data
@app.route("/api/v1.0/end_date")
def end_date():
##################
##working on it!##
##################
    session.close()


if __name__ == '__main__':
    app.run(debug=True)