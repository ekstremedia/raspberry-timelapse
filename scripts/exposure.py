import pytz
import json


exposure_max = 6000000
exposure_min = 4000

with open('solartimes.json') as json_file:
    solardata = json.load(json_file)
    day = solardata["01-01"]
    print(day)