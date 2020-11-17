import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

import datetime as dt

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end><br/>"
    )


@app.route("/api/v1.0/precipitation")
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of date and precipitation data"""
    # Columns for selection
    sel = [Measurement.date
        ,Measurement.prcp]

    # Retrieving the data and precipitation scores
    prcp_data = session.query(*sel).\
                order_by(Measurement.date.asc()).all()
    
    session.close()

    # Convert list of tuples into dictionary
    prcp_dict = {date: prcp for (date, prcp) in prcp_data}

    return jsonify(prcp_dict)


@app.route("/api/v1.0/stations")
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations data"""
    # Columns for selection
    sel = [Station.station
            ,Station.name
            ,Station.latitude
            ,Station.longitude
        ]

    # Retrieving the Station data
    station_data = session.query(*sel).all()
    
    session.close()

    # Convert list of tuples into list
    station_list = list(np.ravel(station_data))

    return jsonify(station_list)


@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    # Calculating the date 1 year ago from the last data point in the database
    Last_Data_Point = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    for row in Last_Data_Point:
        Last_Date = dt.datetime.strptime(row[:], "%Y-%m-%d")
   
    Last_Year_Date = Last_Date.replace(year = Last_Date.year - 1)
   
    st_value_count = session.query(Measurement.station).\
                    group_by(Measurement.station).\
                    order_by(func.count(Measurement.tobs).desc()).\
                    first()
    for row in st_value_count:
        st_max_temp_count = row

    # Columns for selection
    sel = [Measurement.station
            ,Measurement.date
            ,Measurement.tobs
            ]

    # Query to retrieve the Temperature data for the most active station and saving result in pandas dataframe
    Last_Year_Temp_Data = session.query(*sel).\
                    filter(Measurement.station == st_max_temp_count).\
                    filter(func.strftime("%Y-%m-%d", Measurement.date) >= Last_Year_Date).\
                    order_by(Measurement.date.asc()).all()
    session.close()

    # Convert list of tuples into normal list
    temp_list = list(np.ravel(Last_Year_Temp_Data))

    return jsonify(temp_list)

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def temp_stats_by_date_range(start,end=None):
    # Format the date received from api call
    start_date = dt.datetime.strptime(start, "%Y-%m-%d").date()
    if end!=None:
        end_date = dt.datetime.strptime(end, "%Y-%m-%d").date()

    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of stations data"""
    # Columns for selection
    sel = [Measurement.station
            ,Measurement.date
            ,func.min(Measurement.tobs)
            ,func.max(Measurement.tobs)
            ,func.avg(Measurement.tobs)
            ]

    # Retrieving the Station data based on dates in api call
    if end==None:
        station_data = session.query(*sel).\
                    filter(Measurement.date >= start_date).\
                    group_by(Measurement.station, Measurement.date).\
                    all()
    else:
        station_data = session.query(*sel).\
                    filter(Measurement.date >= start_date).\
                    filter(Measurement.date <= end_date).\
                    group_by(Measurement.station, Measurement.date).\
                    all()

    session.close()

    # Convert list of tuples into list
    station_list = list(np.ravel(station_data))

    return jsonify(station_list)

if __name__ == '__main__':
    app.run(debug=True)