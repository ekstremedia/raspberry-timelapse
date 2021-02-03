#!/usr/bin/env /usr/local/bin/python3.9
import pytz
import json
from datetime import datetime, time, timezone, timedelta

tz = pytz.timezone('Europe/Oslo')
#mytz = datetime(2021,12,31)
mytz = datetime.now()
mytz = tz.localize(mytz)
day = mytz.strftime ('%d');                               # 05
month = mytz.strftime ('%m');    
dateStr = day+"-"+month

exposure_max = 6000000
exposure_min = 4000

with open('scripts/solartimes.json') as json_file:
    solardata = json.load(json_file)
    day = solardata[dateStr]
    print(day)