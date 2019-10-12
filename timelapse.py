#!/usr/bin/env python3
from time import sleep
from datetime import datetime, date, time
from picamera import PiCamera
import os
#import time
import threading
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
    try:
        filePrefix = config['filePrefix']
    except KeyError:
        filePrefix = ""
    infoMsg("Filename prefix: "+greenText(filePrefix))

    try:
        iso = config['iso']
    except KeyError:
        iso = 200

    try:
        interval = config['interval']
    except KeyError:
        interval = 10


    # Set folder for timelapse photos
    def capture():
        if not os.path.exists(filePath):
            os.makedirs(filePath)
            infoMsg("Created folder: " + greenText(filePath))

        infoMsg("Set timelapse-folder to: "+greenText(filePath))
        infoMsg("Interval set to every: "+greenText(str(interval))+" second.")
        infoMsg("")
        infoMsg("Starting timelapse in "+greenText(str(interval))+ " seconds")
        while (not sleep(interval)):
            #Date and time settings
            now = datetime.now()
            today = os.path.join(filePath,str(now.year),str('%02d'%now.month),str('%02d'%now.day))
            time = str('%02d'%now.hour)+"_"+str('%02d'%now.minute)+"_"+str('%02d'%now.second)
            if not os.path.exists(today):
                os.makedirs(today)
                infoMsg("Created folder: " + greenText(today))
            fileName = os.path.join(today+"/"+filePrefix+"_"+time+".jpg")
            camera = PiCamera()
            set_camera_options(camera)
            # Capture a picture.
            camera.capture(fileName.format(image_number))
            infoMsg('Captured '+fileName)
            camera.close()



def set_camera_options(camera):
    # Set camera resolution.

    if config['resolution']:
        camera.resolution = (
            config['resolution']['width'],
            config['resolution']['height']
        )
        camera.iso = iso
    if config['shutter_speed']:
        camera.shutter_speed = config['shutter_speed']
        # Sleep to allow the shutter speed to take effect correctly.
        sleep(1)
        camera.exposure_mode = 'off'

    if config['white_balance']:
        camera.awb_mode = 'off'
        camera.awb_gains = (
            config['white_balance']['red_gain'],
            config['white_balance']['blue_gain']
        )
    return camera


def capture_image(fileName):
    try:
        global image_number

        # Set a timer to take another picture at the proper interval after this
        # picture is taken.
        thread = threading.Timer(config['interval'], capture_image).start()
        # Start up the camera.
        camera = PiCamera()
        set_camera_options(camera)
        # Capture a picture.
        camera.capture(fileName.format(image_number))
        infoMsg('Captured '+fileName)
        camera.close()

    except SystemExit:
        infoMsg('\nTime-lapse capture cancelled.\n')

# Initalize Camera
camera = PiCamera()
capture()
# Set camera config if config is loaded

#if loadedConf:
#   set_camera_options(camera)

#print(camera.iso)
#rint dir(camera)









