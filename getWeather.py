#!/usr/bin/env python3.9
import urllib.request
import json
import logging
import os
from datetime import datetime, date, time
homedir = "/home/pi/raspberry-timelapse/"
logdir = os.path.join(homedir, "logs")
logfilename = "getWeather.log"
logfile = os.path.join(logdir, logfilename)
if not os.path.exists(logdir):
    os.makedirs(logdir)
    print("Made logs/ directory")

logging.basicConfig(filename=logfile, encoding="utf-8", level=logging.DEBUG)

def log(text):
    now = datetime.now()
    today = str('%02d' % now.day) + "." + str('%02d' % now.month) + "." + str(now.year) + " "
    timeprint = today + str('%02d' % now.hour) + ":" + str('%02d' % now.minute) + ":" + str('%02d' % now.second)
    dateStr = timeprint + ": "
    logging.info(dateStr + text)

filename = os.path.join(homedir, 'netatmo.json')
url = 'https://ekstremedia.no/nesthus2020/public/data/netatmoStatus'
try:
    req = urllib.request.Request(url)
    r = urllib.request.urlopen(req).read()
    cont = json.loads(r.decode('utf-8'))
    weatherList = {}
    temp = {'temperature': cont['body']['devices'][0]['modules'][0]['dashboard_data']['Temperature']}
    humidity = {'humidity': cont['body']['devices'][0]['modules'][0]['dashboard_data']['Humidity']}
    temp_trend = {'temp_trend': cont['body']['devices'][0]['modules'][0]['dashboard_data']['temp_trend']}
    pressure = {'pressure': cont['body']['devices'][0]['dashboard_data']['Pressure']}
    pressure_trend = {'pressure_trend': cont['body']['devices'][0]['dashboard_data']['pressure_trend']}
    co2 = {'co2': cont['body']['devices'][0]['dashboard_data']['CO2']}

    weatherList.update(temp)
    weatherList.update(humidity)
    weatherList.update(temp_trend)
    weatherList.update(pressure)
    weatherList.update(pressure_trend)
    weatherList.update(co2)

    logTemp = "Temp: "+str(weatherList['temp'])+"c"
    logHumidity = "Humidity: "+str(weatherList['humidity'])

    logOut = logTemp +" "+logHumidity
    with open(filename, 'w') as outfile:
        json.dump(cont, outfile)
        log(logOut)
except:
    log("Could not download file")





