import requests
import json
import datetime 
import time
from time import mktime
import pytz

def get_temperature():

  Dict_of_temps = {}

  r = requests.get("https://api.open-meteo.com/v1/forecast?latitude=33.99&longitude=-83.72&hourly=temperature_2m")
  data = json.loads(r.text)
  for i,j in zip(data["hourly"]["temperature_2m"], data["hourly"]["time"]):
    Dict_of_temps[j] = i

  time_key = time.strftime("%Y-%m-%dT%T", time.gmtime())
  
  time_key = time_key.split(":")
  time_key = time_key[0] + ":00"

  temp = Dict_of_temps[time_key]
  return(round((temp * 1.8) + 32))
  
if __name__ == "__main__":
  print(get_temperature())

