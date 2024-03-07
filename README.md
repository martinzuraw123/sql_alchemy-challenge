In this assignment you have to  conduct a climate analysis using Python, SQLAlchemy, and Flask. In part one analyze and explore climate data using the following:
Use the SQLAlchemy create_engine() function to connect to your SQLite database.
Use the SQLAlchemy automap_base() function to reflect your tables into classes, and save references to the classes named station and measurement.
Link Python to the database by creating a SQLAlchemy session.
Perform a precipitation analysis and then a station analysis.
Precipitation Analysis
Find the most recent date in the dataset.
Get the previous 12 months of precipitation data.
Load the query results into a Pandas DataFrame, sort it, and plot the results.
Use Pandas to print the summary statistics for the precipitation data.
Station Analysis
Design a query to calculate the total number of stations in the dataset.
Design a query to find the most-active stations.
Design a query that calculates the lowest, highest, and average temperatures for the most-active station.
Design a query to get the previous 12 months of temperature observation (TOBS) data, and plot the results as a histogram.
In part two of the assignment design your climate app.Design a Flask API based on the queries that you developed. Include the following routes:
/: Start at the homepage, list all available routes.
/api/v1.0/precipitation: Convert the precipitation analysis results to a dictionary and return the JSON representation.
/api/v1.0/stations: Return a JSON list of stations from the dataset.
/api/v1.0/tobs: Query the most-active station for the previous year's temperature observations and return a JSON list.
/api/v1.0/<start> and /api/v1.0/<start>/<end>: Return JSON lists of temperature statistics for a specified start date or start-end range.
