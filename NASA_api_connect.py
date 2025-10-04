import requests
import pandas as pd

url = "https://api.nasa.gov/neo/rest/v1/feed?start_date=2010-09-07&end_date=2010-09-08&api_key=37Cui5Adua2tZknDatSnrZCvudydLARTmddHjtiG"
#headers = {"Authorization": "Bearer TU_TOKEN"}  # si requiere autenticación

response = requests.get(url, headers=headers)
data = response.json()  # o response.text si es CSV directo

df = pd.DataFrame(data)
df.to_csv("datos.csv", index=False)
