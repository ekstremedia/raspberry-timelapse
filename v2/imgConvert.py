#!/usr/bin/env /usr/local/bin/python3.10

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
# from virtualTimer import getCurrentExposure

localStorage = localStoragePy('ekstremedia-timelapse-exposure', 'sqlite')
tz = pytz.timezone('Europe/Oslo')
#mytz = datetime(2021,12,31)
mytz = datetime.datetime.now()
mytz = tz.localize(mytz)
day = mytz.strftime ('%d. %b %Y %H:%M')
config = yaml.safe_load(open(os.path.join(sys.path[0], "config.yml")))
try:
    annotation = config['camera_name']
except KeyError:
    annotation = ""
topText = f"{annotation} - {day}"

homedir = sys.path[0]
last_image_file = os.path.join(homedir, "logs/last_image.log")
print(last_image_file)
with open(last_image_file) as f:
    filename = f.readline()
print(filename)

fileout = filename
if os.path.exists(filename):

    cmd = "convert "+ filename+ " -undercolor 'rgba(0,0,0,0.4)' -fill white -gravity North -pointsize 20 -annotate +5+5 \' " + topText + "\' " + fileout
    os.system(cmd)
    log("imgConvert done")
else:
    log("imgConvert could not find file")
