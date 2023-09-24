from ovos_utils import classproperty
from ovos_utils.intents import IntentBuilder
from ovos_utils.process_utils import RuntimeRequirements
from ovos_workshop.decorators import intent_handler
from ovos_workshop.skills import OVOSSkill
import requests
import json
import datetime 
import time
from time import mktime
import pytz
import logging

class TemperatureSkill(OVOSSkill):
    def __init__(self, *args, **kwargs):
        """The __init__ method is called when the Skill is first constructed.
        Note that self.bus, self.skill_id, self.settings, and
        other base class settings are only available after the call to super().

        This is a good place to load and pre-process any data needed by your
        Skill, ideally after the super() call.
        """
        super().__init__(*args, **kwargs)
        self.learning = True

    @classproperty
    def runtime_requirements(self):
        return RuntimeRequirements(
            internet_before_load=True,
            network_before_load=True,
            gui_before_load=False,
            requires_internet=True,
            requires_network=True,
            requires_gui=False,
            no_internet_fallback=True,
            no_network_fallback=True,
            no_gui_fallback=True,
        )

    @property
    def get_my_setting(self):
        """Dynamically get the my_setting from the skill settings file.
        If it doesn't exist, return the default value.
        This will reflect live changes to settings.json files (local or from backend)
        """
        latitude = self.settings.get("latitude", "default_value")
        longitude = self.settings.get("longitude", "default_value")
        
        """"return self.settings.get("my_setting", "default_value")"""
        return latitude, longitude

    @intent_handler(IntentBuilder("TemperatureIntent").require("TemperatureKeyword"))
    def handle_temperature_intent(self, message):
        """This is an Adapt intent handler, it is triggered by a keyword."""
        self.log.info("Happiness: keyword handler")
        current_temperature, forecast = self.get_temperature()
        self.log.info(current_temperature)
        self.log.info(forecast)
        self.speak_dialog("how.cold.is.it",{"temperature": current_temperature, "forecast":forecast})

    @intent_handler("HowColdIsIt.intent")
    def handle_how_cold_is_it_intent(self, message):
        """This is a Padatious intent handler.
        It is triggered using a list of sample phrases."""
        self.log.info("Happiness: phrase handler")
        current_temperature, forecast = self.get_temperature()
        self.speak_dialog("how.cold.is.it", {"temperature": current_temperature, "forecast": forecast})

    @intent_handler(IntentBuilder("HumidityIntent").require("HumidityKeyword"))
    def handle_humidity_intent(self, message):
        """Skills can log useful information. These will appear in the CLI and
        the skills.log file."""
        self.log.info("Happiness: 80")
        self.speak_dialog("humidity")

    def stop(self):
        """Optional action to take when "stop" is requested by the user.
        This method should return True if it stopped something or
        False (or None) otherwise.
        If not relevant to your skill, feel free to remove.
        """
        pass
        
    def get_temperature(self):
    
         self.log.info("Begin get_temperature")

         data = {}
         
         latitude = self.settings.get("latitude", "default_value")  
         
         self.log.info(latitude)  
         
         longitude = self.settings.get("longitude", "default_value")
         
         self.log.info(longitude) 
       
         #nws = requests.get("https://api.weather.gov/points/" + latitude + ","  + longitude)
         
         try:
             nws = requests.get("https://api.weather.gov/points/" + latitude + ","  + longitude)
             nws.raise_for_status()
         except:
             return None, None
           
         self.log.info(nws.status_code)
    
         data = json.loads(nws.text)
  
         nws1 = requests.get(data["properties"]["forecast"])
         
         try:
             nws1 = requests.get(data["properties"]["forecast"])
             nws1.raise_for_status()
         except:
             return None, None
         
         self.log.info(nws.status_code)
  
         data1 = json.loads(nws1.text)
         data1 = data1["properties"]["periods"]

         dl = data1[0]
  
         nws2 = requests.get(data['properties']['forecastHourly'])
         
         try:
             nws2 = requests.get(data['properties']['forecastHourly'])
             nws2.raise_for_status()    
         except requests.exceptions.HTTPError as errh:
             return None, None
    
         self.log.info(nws.status_code)

         data2 = json.loads(nws2.text)

         dd = data2["properties"]["periods"][0]
         
         self.log.info(dd['temperature'])
         
         self.log.info(dl['detailedForecast'])
         
         forecast = dl['detailedForecast'].replace("mph","miles per hour")
  
         return dd['temperature'], forecast 
