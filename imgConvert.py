#!/usr/bin/env /usr/local/bin/python3.9

import os
import sys
from shutil import copyfile
import json
import subprocess 
from logger import *
import pytz
import datetime
import yaml
from localStoragePy import localStoragePy

localStorage = localStoragePy('ekstremedia-timelapse-exposure', 'sqlite')
tz = pytz.timezone('Europe/Oslo')
#mytz = datetime(2021,12,31)
mytz = datetime.datetime.now()
mytz = tz.localize(mytz)
day = mytz.strftime ('%d. %b %Y %H:%M:%S')
config = yaml.safe_load(open(os.path.join(sys.path[0], "config.yml")))
try:
    annotation = config['annotation']
except KeyError:
    annotation = ""
topText = f"{annotation} - {day}"


# f = open(last_image_file, "w+")
# f.write(f"/var/www/html/bilder/2021/02/05/sigerfjord_cam_01_20_21_26.jpg")
# f.close()




homedir = sys.path[0]
last_image_file = os.path.join(homedir, "logs/last_image.log");
#last_shutterspeed =  os.path.join(homedir, "logs/last_shutter.log");
last_shutter = getCurrentExposure()
print(last_image_file)
with open(last_image_file) as f:
    filename = f.readline()
print(filename)

# with open(last_shutterspeed) as sh:
#     last_shutter = sh.readline()
# last_shutter = subprocess.getoutput(shutter_cmd)
#print(last_shutter)
fileout = filename
if os.path.exists(filename):
    netatmoFile = "netatmo.json"
    netatmo = os.path.join(homedir, netatmoFile)
    if not os.path.exists(netatmo):
        print("File doesnt exists, downloading")
        cmd = ['python3.9', 'getWeather.py']
        subprocess.Popen(cmd).wait()

    with open(netatmo, 'r') as json_file:
        data = json.load(json_file)

    weatherList = {}

    temp = { 'temperature': data['body']['devices'][0]['modules'][0]['dashboard_data']['Temperature'] }
    humidity = { 'humidity': data['body']['devices'][0]['modules'][0]['dashboard_data']['Humidity'] }
    temp_trend = { 'temp_trend': data['body']['devices'][0]['modules'][0]['dashboard_data']['temp_trend'] }
    pressure = { 'pressure': data['body']['devices'][0]['dashboard_data']['Pressure'] }
    pressure_trend = { 'pressure_trend': data['body']['devices'][0]['dashboard_data']['pressure_trend'] }
    rain = { 'rain':  data['body']['devices'][0]['modules'][1]['dashboard_data']['Rain'] }

    weatherList.update(temp)
    weatherList.update(humidity)
    weatherList.update(temp_trend)
    weatherList.update(pressure)
    weatherList.update(pressure_trend)
    weatherList.update(rain)

    logTemp = "Temp: " + str(weatherList.get('temperature')) + " c" 
    logPressure = "Trykk: " + str(weatherList.get('pressure')) + " mb" 
    logPressureTrend = "Trykk-trend: " + str(weatherList.get('pressure_trend')) 
    logHumidity = "Fuktighet: " + str(weatherList.get('humidity')) + " %" 
    logRain = "Nedbør: " + str(weatherList.get('rain')) + " mm" 
    logTempTrend = "Temp-trend: " + str(weatherList.get('temp_trend'))
    iso = localStorage.getItem('iso');
    cmd = "convert "+ filename+ " -undercolor 'rgba(0,0,0,0.4)' -fill white -gravity NorthWest -pointsize 16 -annotate +10+20 \'" + logTemp + "\' " + fileout
    os.system(cmd)
    log(cmd)
    cmd = "convert "+ filename+ " -undercolor 'rgba(0,0,0,0.4)' -fill white -gravity NorthWest -pointsize 16 -annotate +10+40 \'" + logTempTrend + "\' " + fileout
    os.system(cmd)
    cmd = "convert "+ filename+ " -undercolor 'rgba(0,0,0,0.4)' -fill white -gravity NorthWest -pointsize 16 -annotate +10+60 \'" + logPressure + "\' " + fileout
    os.system(cmd)
    cmd = "convert "+ filename+ " -undercolor 'rgba(0,0,0,0.4)' -fill white -gravity NorthWest -pointsize 16 -annotate +10+80 \'" + logPressureTrend + "\' " + fileout
    os.system(cmd)
    cmd = "convert "+ filename+ " -undercolor 'rgba(0,0,0,0.4)' -fill white -gravity NorthWest -pointsize 16 -annotate +10+100 \'" + logHumidity + "\' " + fileout
    os.system(cmd)
    cmd = "convert "+ filename+ " -undercolor 'rgba(0,0,0,0.4)' -fill white -gravity NorthWest -pointsize 16 -annotate +10+120 \'" + logRain + "\' " + fileout
    os.system(cmd)
    cmd = "convert "+ filename+ " -undercolor 'rgba(0,0,0,0.4)' -fill white -gravity NorthWest -pointsize 16 -annotate +10+140 \'Exposure: " + last_shutter + "\' " + fileout
    os.system(cmd)
    cmd = "convert "+ filename+ " -undercolor 'rgba(0,0,0,0.4)' -fill white -gravity NorthWest -pointsize 16 -annotate +10+160 \'Iso: " + iso + "\' " + fileout
    os.system(cmd)
    cmd = "convert "+ filename+ " -undercolor 'rgba(0,0,0,0.4)' -fill white -gravity North -pointsize 20 -annotate +5+5 \' " + topText + "\' " + fileout
    os.system(cmd)
    log("imgConvert done")
else:
    log("imgConvert could not find file")