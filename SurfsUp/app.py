# Import the dependencies.
from flask import Flask, jsonify
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from flask import Flask, jsonify, request
from sqlalchemy.ext.automap import automap_base
from sqlalchemy import create_engine, inspect, func
import datetime as dt
###################################################################################################################
# Database Setup
###################################################################################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)
# Base.prepare(autoload_with=engine)
# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
# Create our session (link) from Python to the DB
Session = sessionmaker(bind=engine)
session = Session()
###################################################################################################################
# Flask Setup
###################################################################################################################
app = Flask(__name__)
###################################################################################################################
# Flask Routes
###################################################################################################################
# Start at the homepage.
# List all the available routes.
@app.route('/')
def home():
    return "<h1 style='color:blue;'>Welcome to the home page</h1><br> \
            <u>You can request data from these end-points:</u><br> \
            Last 12-months of precipitaion data from: <b><a href='http://127.0.0.1:5000/api/v1.0/precipitation'>/api/v1.0/precipitation</a></b><br>\
            List of stations from:  <b><a href='http://127.0.0.1:5000/api/v1.0/stations'>/api/v1.0/stations</b></a><br>\
            List of temperature observations for the previous year from: <b><a href='http://127.0.0.1:5000/api/v1.0/tobs'>/api/v1.0/tobs</a></b><br>\
            Min, Average & Max temperature for a specified start date from:  <b>/api/v1.0/'YYYY-MM-DD' </b><br>\
            Min, Average & Max temperature for a specified range of dates from:  <b>/api/v1.0/'YYYY-MM-DD/YYYY-MM-DD' </b>"
###################################################################################################################
# Convert the query results from your precipitation analysis 
# (i.e. retrieve only the last 12 months of data) to a dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
@app.route('/api/v1.0/precipitation')
def precipitation():
    print('LAST 12 MONTHS OF PRECIPITATION DATA WAS REQUESTED')
    most_recent_date = session.query(func.max(Measurement.date)).one()[0] 
    mrd_dt_object = dt.datetime.strptime(most_recent_date, '%Y-%m-%d').date()
    prev_twelve_mo = (mrd_dt_object) - (dt.timedelta(days=365))
    last_12_months = session.query(Measurement.date, Measurement.prcp).filter(Measurement.date >= prev_twelve_mo).order_by(Measurement.date).all()
    last_12_months = dict(last_12_months)
    return jsonify(last_12_months)
###################################################################################################################
# Return a JSON list of stations from the dataset.
@app.route('/api/v1.0/stations')
def stations():
    print('A LIST OF STATIONS WAS REQUESTED')
    stations =session.query(Station.station).all()
    list_of_stations = [e[0] for e in stations]
    return jsonify(list_of_stations)

###################################################################################################################
# Query the dates and temperature observations of the most-active station for the previous year of data.
# Return a JSON list of temperature observations for the previous year.
@app.route('/api/v1.0/tobs')
def tobs():
    print('DATES AND TEMPERATURES OBSERVATIONS OF THE MOST_ACTIVE STATION FOR THE PREVIOUS YEAR DATA WAS REQUESTED')
    most_recent_date = session.query(func.max(Measurement.date)).one()[0] 
    mrd_dt_object = dt.datetime.strptime(most_recent_date, '%Y-%m-%d').date()
    prev_twelve_mo = (mrd_dt_object) - (dt.timedelta(days=365))
    most_active = session.query(Measurement.station).group_by(Measurement.station).order_by(func.count(Measurement.station).desc()).first()[0]
    tobs =session.query(Measurement.date, Measurement.tobs).filter(Measurement.date >= prev_twelve_mo)\
                .filter(Measurement.station == most_active).order_by(Measurement.date).all()        
    lst = []
    initialDict = ({'most_active_station':most_active})
    lst.append(initialDict)
    secondDict = ({"Dates":"Temperature"})
    lst.append(secondDict)
    tobs = dict(tobs)
    lst.append(tobs)
    return jsonify(lst)

###################################################################################################################
# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
@app.route('/api/v1.0/<start>/')
def start(start):
    print(f'NIMINUM, AVERATAE AND MAXIMUM TEMPERATURES FOR DATE: {start} WAS REQUESTED')
    temps = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    temp = session.query(*temps).filter(Measurement.date >= start).all()
    # d = {
    #     "0 Date": start,
    #     "1. Minimum Temperature": temp[0][0],
    #     "2. Average Termperature": round(temp[0][1], 2),
    #     "3. Maximum Termperature": temp[0][2]
    # }
    #Created a dictionary above but then I Read it calls for a "JSON LIST"
    l = list()
    l.append("Min Temp " + str(temp[0][0]))
    l.append("Ave Temp " + str(round(temp[0][1], 2)))
    l.append("Max Temp " + str(temp[0][2]))
    return jsonify(l)

###################################################################################################################
# Return a JSON list of the minimum temperature, the average temperature, and the maximum temperature for a specified start or start-end range.
# For a specified start, calculate TMIN, TAVG, and TMAX for all the dates greater than or equal to the start date.
# For a specified start date and end date, calculate TMIN, TAVG, and TMAX for the dates from the start date to the end date, inclusive.
@app.route('/api/v1.0/<start>/<end>')
def start_end(start, end):
    print(f'NIMINUM, AVERATAE AND MAXIMUM TEMPERATURES FOR DATE RANGE: {start} TO {end} WAS REQUESTED')
    temps = [func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)]
    temp =  session.query(*temps).filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    l = list()
    l.append("Start Date " + str(start))
    l.append("End Date " + str(end))
    l.append("Min Temp " + str(temp[0][0]))
    l.append("Ave Temp " + str(round(temp[0][1], 2)))
    l.append("Max Temp " + str(temp[0][2]))
    return jsonify(l)

if __name__ == '__main__':
    app.run(debug=True)



