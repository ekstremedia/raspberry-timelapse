#!/usr/bin/env python3.9
import urllib.request
import json
import logging
import os
from datetime import datetime, date, time

logdir = "logs";
if not os.path.exists(logdir):
    os.makedirs(logdir)
    print("Made logs/ directory")

logging.basicConfig(filename="logs/getWeather.log", encoding="utf-8", level=logging.DEBUG)

def log(text):
    now = datetime.now()
    today = str('%02d' % now.day) + "." + str('%02d' % now.month) + "." + str(now.year) + " "
    timeprint = today + str('%02d' % now.hour) + ":" + str('%02d' % now.minute) + ":" + str('%02d' % now.second)
    dateStr = timeprint + ": "
    logging.info(dateStr + text)

filename = 'netatmo.json'
try:
  url = 'https://ekstremedia.no/nesthus2020/public/data/netatmoStatus'
  req = urllib.request.Request(url)
  r = urllib.request.urlopen(req).read()
  cont = json.loads(r.decode('utf-8'))
  #print(cont['body']['devices'][0]['station_name'])
  temp = cont['body']['devices'][0]['modules'][0]['dashboard_data']['Temperature']
  with open(filename, 'w') as outfile:
    json.dump(cont, outfile)
    log("Write new data to "+filename + " - Temp: "+str(temp)+"c")
except:
  log("Could not download file")
