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
            internet_before_load=False,
            network_before_load=False,
            gui_before_load=False,
            requires_internet=False,
            requires_network=False,
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
        return self.settings.get("my_setting", "default_value")

    @intent_handler(IntentBuilder("TemperatureIntent").require("TemperatureKeyword"))
    def handle_temperature_intent(self, message):
        """This is an Adapt intent handler, it is triggered by a keyword."""
        self.log.info("Happiness: keyword handler")
        current_temperature = get_temperature()
        self.speak_dialog("how.cold.is.it",{"temperature": current_temperature})

    @intent_handler("HowColdIsIt.intent")
    def handle_how_cold_is_it_intent(self, message):
        """This is a Padatious intent handler.
        It is triggered using a list of sample phrases."""
        self.log.info("Happiness: phrase handler")
        current_temperature = get_temperature()
        self.speak_dialog("how.cold.is.it",{"temperature": current_temperature})

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
