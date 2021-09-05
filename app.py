#Imports
 [1]:
#import dependencies
%matplotlib inline
from matplotlib import style
style.use('fivethirtyeight')
import matplotlib.pyplot as plt

import numpy as np
import pandas as pd

import datetime as dt

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
Base.prepare(engine, reflect = True)

# Save reference to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app=Flask(__name__)


#################################################
# Flask Routes
#################################################

#Have the home page return the information of the different routes
@app.route("/")
def intro():

    """List all apis"""
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
        )  
#################################################
    
@app.route("/api/v1.0/precipitation")    
def precipitation():
    """Last Year of Percipitation Data"""
    session = Session(engine)

    # Find last date in database from Measurements
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Convert last date string to date
    last_date

     # Perform a query to retrieve the data and precipitation scores
    one_year_ago = session.query(Measurement.date).order_by(Measurement.date.desc()).first()    
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Design a Query to Retrieve the Last 12 Months of Precipitation Data Selecting Only the `date` and `prcp` Values
    prcp_data = session.query(Measurement.date, Measurement.prcp).\ filter(Measurement.date >= one_year_ago).\
    order_by(Measurement.date).all()

    # Perform a Query to Retrieve the Data and Precipitation Scores
    all_scores = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date.desc()).all()  

@app.route("/api/v1.0/stations")
def stations():
    """List of Weather Stations"""
    session = Session(engine)

    # Select station names from stations table
    active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\ 
    order_by(func.count(Measurement.station).desc()).all()

    # Return JSONIFY List of Stations
    
    return jsonify(active_stations)
    
@app.route("/api/v1.0/tobs")
def tobs():
        """Temperature Observations for Top Station for Last Year"""
    
    session = Session(engine)
    
    # Find last date in database from Measurements 
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()

    # Calculate date one year after last date using timedelta datetime function
    one_year_ago = dt.date(2017,8,23) - dt.timedelta(days=365)

    # Design a Query to Retrieve the Last 12 Months of Precipitation Data Selecting Only the `date` and `prcp` Values
    prcp_data = session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= one_year_ago).\
    order_by(Measurement.date).all()

    # Perform a Query to Retrieve the Data and Precipitation Scores
    all_scores = session.query(Measurement.date, Measurement.prcp).order_by(Measurement.date.desc()).all()
  
    # Save the Query Results as a Pandas DataFrame and Set the Index to the Date Column & Sort the Dataframe Values by `date`
    prcp_df = pd.DataFrame(prcp_data, columns=["Date","Precipitation"])
    prcp_df.set_index("Date", inplace=True,)
    prcp_df.head()
   
   # Use Pandas to Calculate the Summary of the Precipitation Data
    prcp_df.describe()
    
    # Design a Query to show the number of Stations in the Dataset
    station_count = session.query(Measurement.station).distinct().count()
    station_count

    # Design a Query to Find the Most Active Station(s)
    # List the Station(s) and Count in Descending Order
    # Which Station Had the Highest Number of Observations?
    active_stations = session.query(Measurement.station, func.count(Measurement.station)).\
    group_by(Measurement.station).\
    order_by(func.count(Measurement.station).desc()).all()

    # Query for the dates and temperature observations from a year from the last data point.
    # Return a JSON list of Temperature Observations (tobs) for the previous year.
    tobs_data = session.query(Measurement.tobs).\
    filter(Measurement.date >= one_year_ago).\
    filter(Measurement.station == "USC00519281").\
    order_by(Measurement.date).all()
    
@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def stats(start=None, end=None):
    session = Session(engine)

    ### Return TMIN, TAVG, TMAX###

    sel = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    
    # Calculate TMIN, TVAG, TMAX for dates greater than start
   return session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start_date).filter(Measurement.date <= end_date).all()
        (calc_temps('2012-02-28', '2012-03-05'))

    # Calculate the total amount of rainfall per weather station for your trip dates using the previous year's matching dates.
    # Sort this in descending order by precipitation amount and list the station, name, latitude, longitude, and elevation
    query_columns = [Station.station, Station.name, Station.latitude, 
       Station.longitude, Station.elevation, func.sum(Measurement.prcp)]

    results = session.query(*query_columns).\
    filter(Measurement.station == Station.station).\
    filter(Measurement.date >= first_date).\
    filter(Measurement.date <= last_date).\
    group_by(Station.name).order_by(func.sum(Measurement.prcp).desc()).all()
    # Convert Query object to df
    stations_table = pd.DataFrame(np.array(station_rain))

    # Rename the columns
    stations_table = stations_table.rename(columns={0: "Station", 1: "Location", 
    2: "Total Precipitation", 3: "Latitude", 4: "Longitude", 5: "Elevation"})
    stations_table

    ## Set the start and end date for the trip
    trip_dates=['08-05','08-06','08-07','08-08','08-09',
            '08-10','08-11','08-12','08-13','08-14','08-15']
    normal_temps=[]
    def daily_normals(date):
    sel = [func.min(Measurement.tobs), 
           func.round(func.avg(Measurement.tobs),2), 
           func.max(Measurement.tobs)]
    return session.query(*sel).filter(func.strftime("%m-%d", Measurement.date) == date).all()

    # Set the min_temp, avg_temp, high_temp
    daily_normals = pd.DataFrame(normal_temps,columns=['min_temp','avg_temp','high_temp'],
    index=trip_dates)
    daily_normals.index.name = 'Dates'
    daily_normals
    for i in trip_dates:
    normal_temps.append(daily_normals(i)[0])
    normal_temps
            
if __name__ == '__main__':
     app.run(debug=True)                            
