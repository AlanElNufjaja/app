import requests
import pandas as pd
from pandas import json_normalize
url = "https://api.nasa.gov/neo/rest/v1/feed?start_date=2012-09-07&end_date=2012-09-08&api_key=37Cui5Adua2tZknDatSnrZCvudydLARTmddHjtiG"
response = requests.get(url)
data = response.json()
df = json_normalize(data["near_earth_objects"]["2012-09-07"]) 


print(df.columns)
df=df.drop(columns=['neo_reference_id', 'name','nasa_jpl_url','is_potentially_hazardous_asteroid','is_sentry_object','links.self','estimated_diameter.meters.estimated_diameter_min',
       'estimated_diameter.meters.estimated_diameter_max',
       'estimated_diameter.miles.estimated_diameter_min',
       'estimated_diameter.miles.estimated_diameter_max',
       'estimated_diameter.feet.estimated_diameter_min',
       'estimated_diameter.feet.estimated_diameter_max','sentry_data','close_approach_data'])
print(df.columns)
df.to_csv("datos_base.csv", index=False)

# Access the list of near earth objects for the specific date
near_earth_objects = data["near_earth_objects"]["2012-09-07"]

# Extract the close_approach_data from each near earth object
all_close_approach_data = []
for obj in near_earth_objects:
    all_close_approach_data.extend(obj["close_approach_data"])

# Normalize the combined list of close approach data
dff = json_normalize(all_close_approach_data)

# If data is a list directly
# df = json_normalize(data)
dff.to_csv("datos_limpios.csv", index=False)

print(dff.columns)
dff=dff.drop(columns=['close_approach_date','epoch_date_close_approach', 
       'relative_velocity.kilometers_per_hour',
       'relative_velocity.miles_per_hour', 'miss_distance.astronomical',
 
       'miss_distance.miles'])
print(dff.columns)
dff.to_csv("datos_base.csv", index=False)
