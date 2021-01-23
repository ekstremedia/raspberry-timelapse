#!/usr/bin/env python3.9
import json
from os import path
import subprocess

filename = 'netatmo.json'
if not path.exists(filename):
    #print("File doesnt exists, downloading")
    cmd = ['python', 'getWeather.py']
    subprocess.Popen(cmd).wait()

with open(filename, 'r') as json_file:
    data = json.load(json_file)

weatherList = {}

temp = { 'temperature': data['body']['devices'][0]['modules'][0]['dashboard_data']['Temperature'] }
humidity = { 'humidity': data['body']['devices'][0]['modules'][0]['dashboard_data']['Humidity'] }
temp_trend = { 'temp_trend': data['body']['devices'][0]['modules'][0]['dashboard_data']['temp_trend'] }
pressure = { 'pressure': data['body']['devices'][0]['dashboard_data']['Pressure'] }
pressure_trend = { 'pressure_trend': data['body']['devices'][0]['dashboard_data']['pressure_trend'] }


weatherList.update(temp)
weatherList.update(humidity)
weatherList.update(temp_trend)
weatherList.update(pressure)
weatherList.update(pressure_trend)

try:
    weatherList.update({'min_temp': data['body']['devices'][0]['modules'][0]['dashboard_data']['min_temp'] })
except KeyError:
    print("No min temp yet")
try:
    weatherList.update({'max_temp': data['body']['devices'][0]['modules'][0]['dashboard_data']['max_temp'] })
except KeyError:
    print("No min temp yet")
try:
    weatherList.update({'rain': data['body']['devices'][0]['modules'][1]['dashboard_data']['Rain'] })
except KeyError:
    print("No min temp yet")

print(weatherList)
