# Use this file to recall the steps
import psycopg2

# Configuration dictionary containing the connection parameters.
# These keys correspond to the standard libpq connection keywords.
db_params = {
    "dbname": "jonathan", # The name of the database we are connecting to
    "user": "jonathan", # The database role (user) to authenticat as
    "password": "", # The password string (empty in our case)
    "host": "localhost", # The hostname or IP address of the server
    "port": "5432" # The TCP port number our server is listening on
}
# 1. Initialize the Connection Object
# The 'conn' variable holds the session instance.
# It establishes the TCP/IP socket with the PostgreSQL server.
conn = psycopg2.connect(**db_params)

# 2. Initialize the Cursor Object
# The 'cur' variable holds the control structure.
# This object is required to send SQL commands across the connection
# and effectively "point" to the results returned by the server.
cur = conn.cursor()

# print("Connection successful.")

# 1. Define the SQL command string
# Variable Name: 'create_table_sql' chosen for explicit descriptiveness.
# Triple quotes (""") allow the string to span multiple lines for readability.
create_table_sql = """
CREATE TABLE IF NOT EXISTS indian_temples (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100),
    deity VARCHAR(50),
    geom GEOMETRY(point, 4326)
);
"""
# id SERIAL PRIMARY KEY:
# SERIAL: A PostgreSQL-specific pseudo-type. It creates an integer column that auto-increments 
# (1, 2, 3...) for every new row. PRIMARY KEY: A constraint that enforces uniqueness. 
# It ensures the id column uniquely identifies each record.

# geom GEOMETRY(Point, 4326):

# GEOMETRY: The PostGIS data type used to store spatial features. 
# (Point): A modifier that restricts the geometry to single coordinate pairs (Points). 
# It rejects Lines or Polygons. 4326: The SRID (Spatial Reference System Identifier). 
# It tells the database that the coordinates are strictly Longitude/Latitude 
# based on the WGS 84 ellipsoid (the GPS standard).

# 2. Execute the SQL command
# The cursor sends the SQL string to the PostgreSQL server for processing.
cur.execute(create_table_sql)
# The cursor is the only object capable of transmitting commands. At this stage,
# the table exists in the current transaction block but is not visible to other users yet.

# 3. Commit the Transaction
# 'conn.commit()' permanently saves the changes to the database.
# Without this, the table creation remains in a temporary state and is discarded 
# when the connection closes.
conn.commit()

print("Table 'indian_temples' created successfully.")

# Define the Data Source
# Variable Name: 'temples_data'
# Structure: A Python list of tuples. tuples are immutable (cannot be changed), 
# making them ideal for representing fixed records (Name, Deity, Lat, Lon).
temples_data = [
    ("Badrinath", "Vishnu", 30.7433, 79.4938),
    ("Kedarnath", "Shiva", 30.7352, 79.0669),
    ("Somnath", "Shiva", 20.8880, 70.4012),
    ("Kashi Vishwanath", "Shiva", 25.3108, 83.0107),
    ("Tirumala", "Vishnu", 13.6832, 79.3471),
    ("Jagannath Puri", "Krishna", 19.8049, 85.8179)
]

# Define the Parameterized SQL Query
# %s: These are placeholders. The database driver will safely insert variables here.
# ST_MakePoint(lon, lat): PostGIS function to create a generic point geometry.
# ST_SetSRID(..., 4326): PostGIS function to assigning the spatial reference system (GPS).
insert_query = """
INSERT INTO indian_temples (name, deity, geom)
VALUES (%s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326));
"""
# Iterate and Execute
# Loop through each tuple in the list to insert rows one by one.
for temple in temples_data:
    name = temple[0]
    deity = temple[1]
    lat = temple[2]
    lon = temple[3]

    # Execute the query
    # CRITICAL: We pass the variables as a second argument (tuple).
    # Note the order: 'lon' must come before 'lat' for ST_MakePoint(x, y).
    cur.execute(insert_query, (name, deity, lon, lat))

# Commit the Transaction
# Saves the inserted rows to the database.
conn.commit()

print(f"Inserted {len(temples_data)} temples successfully.")

# Terminate the session
# 'cur.close()' releases the memory allocated for the cursor.
# 'conn.close()' terminates the TCP/IP socket.
cur.close()
conn.close()
