import argparse
import requests
import json
import logging

def get_temperature():

  data = {}

  try:
    nws = requests.get("https://api.weather.gov/points/" + latitude + ","  + longitude)
    nws.raise_for_status()
  except:
    return []

  logging.info(nws.status_code)
    
  data = json.loads(nws.text)
  
  try:
    nws1 = requests.get(data["properties"]["forecast"])
    nws1.raise_for_status()
  except:
    return []

  logging.info(nws.status_code)
  
  data1 = json.loads(nws1.text)
  data1 = data1["properties"]["periods"]

  dl = data1[0]
  dl1 = data1[1]

  try:
      nws2 = requests.get(data['properties']['forecastHourly'])
      nws2.raise_for_status()    
  except requests.exceptions.HTTPError as errh:
      return [] 
    
  logging.info(nws.status_code)

  data2 = json.loads(nws2.text)

  dd = data2["properties"]["periods"][0] 

  return dl, dd , dl1
  
if __name__ == "__main__":

  parser = argparse.ArgumentParser()

  parser.add_argument('latitude', type=float,
                    help='latitude')
  parser.add_argument('longitude', type=float,
                    help='longitude')                    

  args = parser.parse_args()
  latitude = str(args.latitude)
  longitude = str(args.longitude)
  
  dl, dd, dl1 = get_temperature()
  
  print(dd["shortForecast"])
  print(dd["temperature"])
  print(dl["name"])
  print(dl["temperature"])
  print(dl["detailedForecast"].replace("mph","miles per hour"))
  print(dl1["temperature"])
