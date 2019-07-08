#!/usr/bin/env python3

from datetime import datetime, date, time
#from picamera import PiCamera
import os
import time
import sys
import yaml

red = "\033[1;31;38m"
green = "\033[1;32;38m"
endcolor = "\033[30m"

def errorMsg(text):
    print(red+text+endcolor)

def successMsg(text):
    print(green+text+endcolor)

try:
    config = yaml.safe_load(open(os.path.join(sys.path[0], "config.yml")))
    loadedConf = True
except OSError as e:
    errorMsg("Found no configuration file!")
    successMsg(str(e))
    loadedConf = False

if loadedConf: 
    def set_camera_options(camera):
        # Set camera resolution.
   
        if config['resolution']:
            camera.resolution = (
                config['resolution']['width'],
                config['resolution']['height']
            )
        camera.iso = 100
    
        if config['isloaded']:
            print("Configuration file loaded!")
        else:
            print("Configuration file not loaded!")

# Initalize Camera
#camera = PiCamera()

# Set camera config if config is loaded

#if loadedConf:
#   set_camera_options(camera)

#print(camera.iso)
#rint dir(camera)









