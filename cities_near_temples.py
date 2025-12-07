import pandas as pd
from sqlalchemy import create_engine

# 1. Database Connection
db_connection_url = "postgresql://jonathan:@localhost:5432/jonathan"
engine = create_engine(db_connection_url)

# 2. The Analysis Query
# We cast ::geography to measure in meters.
# 321868 meters is approx 200 miles.
sql = """
SELECT DISTINCT
    c.name AS city_name,
    c.adm1name AS state,
    c.pop_max AS population,
    c.latitude,
    c.longitude
FROM indian_cities c
JOIN indian_temples t
ON ST_DWithin(
    c.geom::geography, 
    t.geom::geography, 
    321868
)
ORDER BY c.pop_max DESC;
"""

print("Running spatial analysis...")

# 3. Execute and Load into Pandas
df = pd.read_sql(sql, engine)

# 4. Show Results
print(f"\nFound {len(df)} cities within 200 miles of a temple.")
print("-" * 50)
print(df.head(10)) # Show top 10 by population

# 5. Save to CSV
df.to_csv("cities_near_temples.csv", index=False)
print("\nResults saved to 'cities_near_temples.csv'")