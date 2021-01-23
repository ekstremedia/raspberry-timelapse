#!/usr/bin/env python3
import urllib.request
import json
import logging

logging.basicConfig(filename="logs/getWeather.log", encoding="utf-8", level=logging.DEBUG)
logging.debug("Test")

filename = 'netatmo.json'
try:
  url = 'https://ekstremedia.no/nesthus2020/public/data/netatmoStatus'
  req = urllib.request.Request(url)
  r = urllib.request.urlopen(req).read()
  cont = json.loads(r.decode('utf-8'))
  print('Status: ' + cont['status'])
  print(cont['body']['devices'][0]['station_name'])
  print(cont['body']['devices'][0]['modules'][0]['dashboard_data']['Temperature'])
  with open(filename, 'w') as outfile:
    json.dump(cont, outfile)
    print("Write new data to "+filename)
except:
  print("Could not download file")
