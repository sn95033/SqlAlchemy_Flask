
#!/usr/bin/env python
# coding: utf-8

# ## SQL ALCHEMY HOMEWORK
# 
#     Step 1 - Climate Analysis and Exploration
#     To begin, use Python and SQLAlchemy to do basic climate analysis and data exploration of your climate database. All of the following analysis should be completed using SQLAlchemy ORM queries, Pandas, and Matplotlib.
# 
#     Use the provided starter notebook and hawaii.sqlite files to complete your climate analysis and data exploration.
#     Choose a start date and end date for your trip. Make sure that your vacation range is approximately 3-15 days total.
# 
#     Use SQLAlchemy create_engine to connect to your sqlite database.
# 
#     Use SQLAlchemy automap_base() to reflect your tables into classes and save a reference to those classes called Station and Measurement.

import numpy as np
import pandas as pd
import datetime as dt

# Use this library to find a date relative to another date
# Reference from Sivakumar Venkatachalam in my tutors repository
from dateutil.relativedelta import relativedelta 

 # Reflect Tables into SQLAlchemy ORM
# Python SQL toolkit and Object Relational Mapper
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect, desc

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///./hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# We can view all of the classes that automap found
# Base.classes.keys()

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

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
def welcome():
    # List all available api routes.
    return (
        f"<h1>Available Routes:</h1><br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/startdate<br/>"
        f"/api/v1.0/startdate/enddate<br/>"
        
    )


@app.route("/api/v1.0/precipitation")

def precipitation():
    # Convert the query results to a Dictionary using date as the key and prcp as the value
    # Return the JSON representation of your dictionary
    all_precip = session.query(Measurement.prcp, Measurement.date).all()

    all_df = pd.DataFrame(all_precip, columns=['Precipitation', 'Date'])

    all_df = all_df.dropna(how="any")
    precip_data = all_df.set_index('Date')
    precip_data_flask = precip_data.to_dict()
    
    return jsonify(precip_data_flask)

@app.route("/api/v1.0/stations")

def stations():
    # Return a JSON list of stations from the stations amd their activity
    # Query all stations
    station_info = session.query(Measurement.station, func.count(Measurement.station).label("Station ct")).\
               group_by(Measurement.station).order_by(desc("Station ct")).all()
    print(station_info)
    
    return jsonify(station_info)

@app.route("/api/v1.0/tobs")

def tobs():
#query for the dates and temperature observations from a year from the last data point.
#   Return a JSON list of Temperature Observations (tobs) for the previous year.

    end_date_str = "2017-08-31"
    end_date = dt.datetime.strptime(end_date_str, "%Y-%m-%d")
    start_date = end_date - relativedelta(years=1)

    station_temp = session.query(Measurement.date, Measurement.tobs).\
            filter(Measurement.date > start_date).all()

    temp_df = pd.DataFrame(station_temp, columns=['Date', 'Temp'])

    temp_df = temp_df.dropna(how="any")
    temp_data = temp_df.sort_values('Date')
    temp_data = temp_df.set_index('Date')
    temp_data_flask = temp_data.to_dict()
    
    return jsonify(temp_data_flask)


@app.route("/api/v1.0/<start>")
def temp_query(start):
    '''Return a JSON list of the minimum temperature, the average temperature,
    and the max temperature for a given start or start-end range.
    When given the start only, calculate TMIN, TAVG, and TMAX for 
    all dates greater than and equal to the start date.'''
    
    start_input = start

    try:
        start_date =  dt.datetime.strptime(start_input, '%Y-%m-%d')

    except:
        print(" Invalid start date or date format. Please input valid date in yyyy-mm-dd format.")
        print(" Using default date. start = 2016-08-23")
        start_input   = '2016-08-23'
        start_date  = dt.datetime.strptime(start_input, '%Y-%m-%d')

    Measurement_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).\
        all()

   # temp_df = pd.DataFrame(station_temp, columns=['Date', 'Temp'])

   # temp_df = temp_df.dropna(how="any")
   # temp_data = temp_df.sort_values('Date')
   # temp_data = temp_df.set_index('Date')
   # temp_data_flask = temp_data.to_dict()
    
    return jsonify(Measurement_temp)

@app.route("/api/v1.0/<start>/<end>")
def temp_st_end(start, end):

    '''Return a JSON list of the minimum temperature, the average temperature,
    and the max temperature for a given start or start-end range.
    When given the start and the end date, calculate the TMIN, TAVG, and TMAX 
    for dates between the start and end date inclusive.'''

    start_input = start
    end_input = end

    try:
        start_date =  dt.datetime.strptime(start_input, '%Y-%m-%d')

    except:
        print(" Invalid start date or date format. Please input valid date in yyyy-mm-dd format.")
        print(" Using default date. start = 2016-08-23")
        start_input   = '2016-08-23'
        start_date  = dt.datetime.strptime(start_input, '%Y-%m-%d')

    try:
        end_date =  dt.datetime.strptime(end_input, '%Y-%m-%d')

    except:
        print(" Invalid end date or date format. Please input valid date in yyyy-mm-dd format.")
        print(" Using default date. end = 2017-08-23")
        end_input   = '2017-08-23'
        end_date  = dt.datetime.strptime(end_input, '%Y-%m-%d')


    Measurement_temp = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
            filter(Measurement.date >= start_date).\
            filter(Measurement.date <= end_date).\
            all()

    
    return jsonify(Measurement_temp)


if __name__ ==  '__main__':
    app.run(debug=True)




