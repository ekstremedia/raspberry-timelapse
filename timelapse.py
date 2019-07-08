#!/usr/bin/env python3

from datetime import datetime, date, time
#from picamera import PiCamera
import os
import time
import sys
import yaml

# Define variables
red = "\033[1;31;38m"
green = "\033[1;32;38m"
endcolor = "\033[0m"
currentDir = os.getcwd()
filePath = ""
# Define functions

def redText(text):
    return red+text+endcolor

def greenText(text):
    return green+text+endcolor

def errorMsg(text):
    print(red+text+endcolor)

def successMsg(text):
    print(green+text+endcolor)

def infoMsg(text):
    print(greenText("*** ")+text)

# Welcome screen
infoMsg(redText("Raspberry")+greenText("Pi")+"-timelapse is loading...")



# Load configuration if present
try:
    config = yaml.safe_load(open(os.path.join(sys.path[0], "config.yml")))
    loadedConf = True
except OSError as e:
    errorMsg("Found no configuration file!")
    successMsg(str(e))
    loadedConf = False

if config['isloaded']:
    infoMsg("Configuration file " + greenText("loaded") + "!")
else:
    print("Configuration file "+redText("not")+" loaded, loading default values.")

if loadedConf:
    try:
        filePath = config['filePath']
    except KeyError:
        filePath = currentDir+"/timelapse/"

    if not os.path.exists(filePath):
        os.makedirs(filePath)
        infoMsg("Created folder: " + greenText(filePath))

    infoMsg("Set timelapse-folder to: "+greenText(filePath))

    now = datetime.now()

    today = os.path.join(filePath,str(now.year),str('%02d'%now.month),str('%02d'%now.day))
    if not os.path.exists(today):
        os.makedirs(today)
        infoMsg("Created folder: " + greenText(today))
    print(today)



    def set_camera_options(camera):
        # Set camera resolution.
   
        if config['resolution']:
            camera.resolution = (
                config['resolution']['width'],
                config['resolution']['height']
            )
        camera.iso = 100



# Initalize Camera
#camera = PiCamera()

# Set camera config if config is loaded

#if loadedConf:
#   set_camera_options(camera)

#print(camera.iso)
#rint dir(camera)









