# Import the dependencies.


import numpy as np
import pandas as pd
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
# Connect to the SQLite database using SQLAlchemy
# I wasn't able to use engine = create_engine("sqlite:///hawaii.sqlite") 
# because it just doesn't work on my computer so this is the solution my TA came up with
engine = create_engine("sqlite:///C:/Users/marti/OneDrive/Desktop/School/SMU-VIRT-DATA-PT-12-2023-U-LOLC/sql_alchemy-challenge/Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()

# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurements = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
Session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)



#################################################
# Flask Routes
#################################################
@app.route('/')
def home():
    # Define the home route that displays available routes
    return (
        "Available Routes:<br/>"
        "/api/v1.0/precipitation<br/>"
        "/api/v1.0/stations<br/>"
        "/api/v1.0/tobs<br/>"
        "/api/v1.0/start_date/<string:start_date><br/>"
        "/api/v1.0/start_date/<string:start_date>/end_date/<string:end_date><br/>"
    )

# Create a sessionmaker instance bound to the engine
Session = sessionmaker(bind=engine)

# Define route to get precipitation data
@app.route('/api/v1.0/precipitation')
def precipitation():
    # Create a new session instance
    session_instance = Session()
    try:
        # Query precipitation data from Measurements table
        results = session_instance.query(Measurements.date, Measurements.prcp)
        precipitation_data = {date: prcp for date, prcp in results}
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        # Close the session to release resources
        session_instance.close()

    return jsonify(precipitation_data)

# Define route to get station data
@app.route('/api/v1.0/stations')
def stations():
    session_instance = Session()
    try:
        # Query station data from Station table
        station_data = session_instance.query(Station.station, Station.name).all()
        result = [{'station': station, 'name': name} for station, name in station_data]
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        session_instance.close()

    return jsonify(result)

# Define route to get temperature observation data
@app.route('/api/v1.0/tobs')
def tobs():
    session_instance = Session()
    try:
        # Query temperature observation data from Measurements table
        results = session_instance.query(Measurements.date, Measurements.tobs)
        tobs_data = {date: tobs for date, tobs in results}
    except Exception as e:
        return jsonify({'error': str(e)})
    finally:
        session_instance.close()

    return jsonify(tobs_data)

# Define route to get temperature stats from a given start date
@app.route('/api/v1.0/start_date/<string:start_date>')
def temp_stats_start(start_date):
    session_instance = Session()
    try:
        # Convert start date string to datetime object
        start_date_obj = dt.datetime.strptime(start_date, '%Y-%m-%d')

        # Query temperature stats from Measurements table
        results = session_instance.query(
            func.min(Measurements.tobs),
            func.avg(Measurements.tobs),
            func.max(Measurements.tobs)
        ).filter(Measurements.date >= start_date_obj).all()

        # Create a dictionary with temperature stats
        temp_stats = {
            'start_date': start_date,
            'min_temperature': results[0][0],
            'avg_temperature': results[0][1],
            'max_temperature': results[0][2]
        }

        return jsonify(temp_stats)

    except Exception as e:
        return jsonify({'error': str(e)})

    finally:
        session_instance.close()

# Define route to get temperature stats between a given start and end date
@app.route('/api/v1.0/start_date/<start_date>/end_date/<end_date>')
def temp_stats_start_end(start_date, end_date):
    session_instance = Session()
    try:
        # Convert start and end dates strings to datetime objects
        start_date_obj = dt.datetime.strptime(start_date, '%Y-%m-%d')
        end_date_obj = dt.datetime.strptime(end_date, '%Y-%m-%d')

        # Query temperature stats from Measurements table
        results = session_instance.query(
            func.min(Measurements.tobs),
            func.avg(Measurements.tobs),
            func.max(Measurements.tobs)
        ).filter(Measurements.date >= start_date_obj, Measurements.date <= end_date_obj).all()

        # Create a dictionary with temperature stats
        temp_stats = {
            'start_date': start_date,
            'end_date': end_date,
            'min_temperature': results[0][0],
            'avg_temperature': results[0][1],
            'max_temperature': results[0][2]
        }

        return jsonify(temp_stats)

    except Exception as e:
        return jsonify({'error': str(e)})

    finally:
        session_instance.close()

# Run the Flask application if executed as the main script
if __name__ == '__main__':
    app.run(debug=True)
