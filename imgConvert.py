#!/usr/bin/env python3.9
import os
import sys
from shutil import copyfile
import json
import subprocess 

homedir = sys.path[0]
filename = sys.argv[1]
fileout = filename
netatmoFile = "netatmo.json"
netatmo = os.path.join(homedir, netatmoFile);

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

cmd = "convert "+ filename+ " -fill white -gravity NorthWest -pointsize 16 -annotate +10+20 \'" + logTemp + "\' " + fileout
os.system(cmd)
cmd = "convert "+ filename+ " -fill white -gravity NorthWest -pointsize 16 -annotate +10+40 \'" + logTempTrend + "\' " + fileout
os.system(cmd)
cmd = "convert "+ filename+ " -fill white -gravity NorthWest -pointsize 16 -annotate +10+60 \'" + logPressure + "\' " + fileout
os.system(cmd)
cmd = "convert "+ filename+ " -fill white -gravity NorthWest -pointsize 16 -annotate +10+80 \'" + logPressureTrend + "\' " + fileout
os.system(cmd)
cmd = "convert "+ filename+ " -fill white -gravity NorthWest -pointsize 16 -annotate +10+100 \'" + logHumidity + "\' " + fileout
os.system(cmd)
cmd = "convert "+ filename+ " -fill white -gravity NorthWest -pointsize 16 -annotate +10+120 \'" + logRain + "\' " + fileout
os.system(cmd)
#copyfile(fileout, '/var/www/html/status.jpg')