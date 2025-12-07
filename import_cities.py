import subprocess
import os

# --- CONFIGURATION SECTION ---
# 1. PATHS
shapefile_path = "./populated_places/ne_10m_populated_places.shp"

# 2. DATABASE CREDENTIALS (FIXED)
# Removed "password=" which was causing the "missing =" syntax error.
# Added "host=localhost" to ensure it finds the local server.
db_connection = "PG:host=localhost dbname=jonathan user=jonathan"

# --- THE COMMAND BUILDER ---
# 3. CONSTRUCT THE COMMAND
cmd = [
    "ogr2ogr",
    "--config", "SHAPE_RESTORE_SHX", "YES", # Keeps the fix for missing .shx file
    "-f", "PostgreSQL",             
    db_connection,                  
    shapefile_path,                 
    "-nln", "indian_cities",        
    "-overwrite",                   
    "-lco", "GEOMETRY_NAME=geom",   
    
    # 4. THE FILTERS
    "-where", "ADM0NAME = 'India'", 
    
    # REMOVED 'wdid' from this list to fix the error
    "-select", "NAME,ADM0NAME,ADM1NAME,ADM0_A3,POP_MAX,LATITUDE,LONGITUDE,FEATURECLA"
]

# --- EXECUTION SECTION ---
print("🚀 Starting import...")
print(f"Reading from: {shapefile_path}")

try:
    # 5. RUN THE COMMAND
    subprocess.check_call(cmd)
    
    print("✅ Success! Table 'indian_cities' created in database 'jonathan'.")

except subprocess.CalledProcessError as e:
    print("❌ The import tool failed.")
    print(f"Error Code: {e.returncode}")
    
except FileNotFoundError:
    print("❌ Error: Python cannot find the 'ogr2ogr' tool.")