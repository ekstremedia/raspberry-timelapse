#!/usr/bin/env python3
from time import sleep
from datetime import datetime, date, time
from picamera import PiCamera
from fractions import Fraction
from shutil import copyfile
import os
# import time
import threading
import sys
import yaml

# Define variables
red = "\033[1;31;38m"
green = "\033[1;32;38m"
endcolor = "\033[0m"
currentDir = os.getcwd()
filePath = ""
total_images = 0


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

if loadedConf:
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
        awb = config['white_balance']
    except KeyError:
        awb = 'cloudy'

    try:
        interval = config['interval']
    except KeyError:
        interval = 10

    try:
        shutter_speed = config['shutter_speed']
    except KeyError:
        shutter_speed = 0

    try:
        copy_last = config['copy_last']
    except KeyError:
        copy_last = False

    try:
        status_filename = config['status_filename']
    except KeyError:
        status_filename = False


    if copy_last:
        infoMsg("Copy image to status image " + greenText("on: ") + " => " + greenText(str(status_filename)))

    def capture():
        if not os.path.exists(filePath):
            os.makedirs(filePath)
            infoMsg("Created folder: " + greenText(filePath))

        infoMsg("Set timelapse-folder to: "+greenText(filePath))
        infoMsg("")
        infoMsg("Starting timelapse in "+greenText(str(interval))+ " ... :) ")
        infoMsg("Shutter:  " + greenText(str(shutter_speed)) + " ISO: " + greenText(str(iso)) + " every " + greenText(
            str(interval)) + " seconds")
        infoMsg("White balance: " + greenText(str(awb)))
        now = datetime.now()
        today = os.path.join(filePath, str(now.year), str('%02d' % now.month), str('%02d' % now.day))
        time = str('%02d' % now.hour) + "_" + str('%02d' % now.minute) + "_" + str('%02d' % now.second)
        if not os.path.exists(today):
            os.makedirs(today)
            infoMsg("Created folder: " + greenText(today))
        fileName = os.path.join(today + "/" + filePrefix + "_" + time + ".jpg")
        take(fileName)

        while not sleep(interval):
            # Date and time settings
            now = datetime.now()
            today = os.path.join(filePath,str(now.year),str('%02d'%now.month),str('%02d'%now.day))
            time = str('%02d'%now.hour)+"_"+str('%02d'%now.minute)+"_"+str('%02d'%now.second)
            if not os.path.exists(today):
                os.makedirs(today)
                infoMsg("Created folder: " + greenText(today))
            fileName = os.path.join(today+"/"+filePrefix+"_"+time+".jpg")
            take(fileName)

def set_camera_options(camera):
    # Set camera resolution.

    if config['resolution']:
        camera.resolution = (
            config['resolution']['width'],
            config['resolution']['height']
        )
        camera.iso = iso
    try:
        camera.shutter_speed = config['shutter_speed']
            # Sleep to allow the shutter speed to take effect correctly.
    except KeyError:
        camera.shutter_speed = 0

    #  sleep(2)

    camera.framerate = Fraction(1, 6)
    #camera.shutter_speed = 6000000

    sleep(2)

    if config['white_balance']:
        camera.awb_mode = config['white_balance']
    else:
        camera.awb_mode = 'cloudy'

    if config['white_balance_gain']:
        camera.awb_gains = config['white_balance_gain']['red_gain'],config['white_balance_gain']['blue_gain']

    camera.exposure_mode = 'off'
    return camera


def take(fileName):
    camera = PiCamera()
    set_camera_options(camera)
    # Capture a picture.
    camera.capture(fileName)
    global total_images
    total_images = total_images+1
    infoMsg('Captured ' + fileName + ' (#' + str(total_images) + ')')
    camera.close()
    global copy_last
    global status_filename
    if (copy_last):
        copyfile(fileName, status_filename)


capture() 

# Set camera config if config is loaded

# if loadedConf:
#   set_camera_options(camera)

# print(camera.iso)









