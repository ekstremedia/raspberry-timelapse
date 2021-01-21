import json
from os import path
import subprocess

filename = 'netatmo.json'
if path.exists(filename):
    print("File exists")
if not path.exists(filename):
    print("File doesnt exists, downloading")
    cmd = ['python', 'getWeather.py']
    subprocess.Popen(cmd).wait()

with open(filename, 'r') as json_file:
    data = json.load(json_file)

print(data['body']['devices'][0]['modules'][0]['dashboard_data']['Temperature'])
print(data['body']['devices'][0]['modules'][0]['dashboard_data']['Humidity'])
print(data['body']['devices'][0]['modules'][0]['dashboard_data']['temp_trend'])
try:
    print(data['body']['devices'][0]['modules'][0]['dashboard_data']['min_temp'])
except KeyError:
    print("No min temp yet")
try:
    print(data['body']['devices'][0]['modules'][0]['dashboard_data']['max_temp'])
except KeyError:
    print("No min temp yet")
try:
    print(data['body']['devices'][0]['modules'][1]['dashboard_data']['Rain'])
except KeyError:
    print("No min temp yet")