#!/usr/bin/env /usr/local/bin/python3.9

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
from logger import *
import locale
import subprocess as sp
from localStoragePy import localStoragePy

# Define variables
red = "\033[1;31;38m"
green = "\033[1;32;38m"
endcolor = "\033[0m"
currentDir = os.getcwd()
filePath = ""
total_images = 0
annotation = ""
homedir = sys.path[0]
shutter_cmd = os.path.join(homedir, 'Timer.py');
localStorage = localStoragePy('ekstremedia-timelapse-exposure', 'sqlite')

def redText(text):
    return red+text+endcolor


def greenText(text):
    return green+text+endcolor


def errorMsg(text):
    print(red+text+endcolor)


def successMsg(text):
    print(green+text+endcolor)


def infoMsg(text):
    now = datetime.now()
    timePrint = str('%02d' % now.hour) + ":" + str('%02d' %
                                                   now.minute) + ":" + str('%02d' % now.second)
    print(greenText("*** ["+timePrint+'] ')+text)


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
    print("Configuration file "+redText("not") +
          " loaded, loading default values.")

if loadedConf:
    try:
        annotation = config['annotation']
    except KeyError:
        annotation = ""
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

    # try:
    #     shutter_speed = config['shutter_speed']
    # except KeyError:
    #     shutter_speed = 0
    shutter_speed = sp.getoutput(shutter_cmd)

    try:
        copy_last = config['copy_last']
    except KeyError:
        copy_last = False

    try:
        status_filename = config['status_filename']
    except KeyError:
        status_filename = False

    try:
        metering = config['metering']
    except KeyError:
        metering = None

    try:
        exposure_mode = config['exposure_mode']
    except KeyError:
        exposure_mode = None

    if copy_last:
        infoMsg("Copy image to status image " + greenText("on: ") +
                "=> " + greenText(str(status_filename)))

    def capture():
        if not os.path.exists(filePath):
            os.makedirs(filePath)
            infoMsg("Created folder: " + greenText(filePath))

        infoMsg("Set timelapse-folder to: "+greenText(filePath))
        infoMsg("")
        infoMsg("Starting timelapse in "+greenText(str(interval)) + " ... :) ")
        infoMsg("Shutter: " + greenText(str(shutter_speed)) + " microseconds, ISO: " + greenText(str(iso)) + ", taking photo every " + greenText(
            str(interval)) + " seconds")
        infoMsg("White balance: " + greenText(str(awb)))
        if metering:
            infoMsg("Metering: " + greenText(str(metering)))
        if exposure_mode:
            infoMsg("Exposure mode: " + greenText(str(exposure_mode)))
        now = datetime.now()
        today = os.path.join(filePath, str(now.year), str(
            '%02d' % now.month), str('%02d' % now.day))
        time = str('%02d' % now.hour) + "_" + str('%02d' %
                                                  now.minute) + "_" + str('%02d' % now.second)
        timePrint = str('%02d' % now.hour) + ":" + str('%02d' %
                                                       now.minute) + ":" + str('%02d' % now.second)
        if not os.path.exists(today):
            os.makedirs(today)
            infoMsg("Created folder: " + greenText(today))
        fileName = os.path.join(today + "/" + filePrefix + "_" + time + ".jpg")
        take(fileName)

        while not sleep(interval):
            # Date and time settings
            now = datetime.now()
            today = os.path.join(filePath, str(now.year), str(
                '%02d' % now.month), str('%02d' % now.day))
            time = str('%02d' % now.hour)+"_"+str('%02d' %
                                                  now.minute)+"_"+str('%02d' % now.second)
            if not os.path.exists(today):
                os.makedirs(today)
                infoMsg("Created folder: " + greenText(today))
            fileName = os.path.join(today+"/"+filePrefix+"_"+time+".jpg")
            take(fileName)


def set_camera_options(camera):
    # Set camera resolution.

    # if config['metering']:
    #     camera.meter_mode = config['metering']

    if config['resolution']:
        camera.resolution = (
            config['resolution']['width'],
            config['resolution']['height']
        )
        # camera.iso = iso

    camera.framerate = Fraction(1, 6)
    # if config['shutter_speed']:
    #     camera.shutter_speed = config['shutter_speed']
    # else:
    #     camera.shutter_speed = 0
    shutter = int(sp.getoutput(shutter_cmd))
    checkCountDown = localStorage.getItem('countDown')
    checkCountUp = localStorage.getItem('countUp')
    print(f"checkCountDown {checkCountDown}")
    print(f"checkCountUp {checkCountUp}")
    if (checkCountDown == 'on' and checkCountUp == 'off'):
        if (shutter < 2000000):
            camera.iso = 100
        if (shutter < 3000000):
            camera.iso = 200
        if (shutter < 4000000):
            camera.iso = 400
        if (shutter < 5000000):
            camera.iso = 600
        if (shutter < 4000):
            camera.iso = 60
    if (checkCountDown == 'off' and checkCountUp == 'on'):
        if (shutter > 2000000):
            camera.iso = 200
        if (shutter > 3000000):
            camera.iso = 400
        if (shutter > 4000000):
            camera.iso = 600
        if (shutter > 5000000):
            camera.iso = 800
        if (shutter < 3000):
            camera.iso = 60
    log(f"Got shutterspeed: {shutter}")
    log(f"Set iso: {camera.iso}")
    logLastShutterSpeed(shutter)
    camera.shutter_speed = int(shutter)
    # camera.shutter_speed = 0

    if config['white_balance']:
        camera.awb_mode = config['white_balance']
    else:
        camera.awb_mode = 'cloudy'

    if config['white_balance_gain']:
        camera.awb_gains = (
            config['white_balance_gain']['red_gain'],
            config['white_balance_gain']['blue_gain']
        )

    # if config['exposure_mode']:
    #     camera.exposure_mode = config['exposure_mode']

    # infoMsg("Preparing camera...")
    sleep(5)
    # infoMsg("Camera ready, starting!")
    return camera


def take(fileName):
    camera = PiCamera()
    set_camera_options(camera)
    # Capture a picture.
    infoMsg("Capturing...")
    now = datetime.now()
    today = str('%02d' % now.day) + "." + str('%02d' % now.month) + " " + str(now.year) + "  "
    timeprint = today + str('%02d' % now.hour) + ":" + str('%02d' % now.minute) + ":" + str('%02d' % now.second)
    camera.annotate_text = annotation + " - " + timeprint
    camera.annotate_text_size = 20
    camera.capture(fileName)
    global total_images
    total_images = total_images+1
    infoMsg('Captured ' + fileName + ' (#' + str(total_images) + ')')
    loglastfile(fileName)
    camera.close()
    global copy_last
    global status_filename
    cmd = os.path.join(homedir, 'imgConvert.py')
    if os.path.exists(fileName):
        log(f"imgconvert_cmd: {cmd}")
        cmd_output = sp.getoutput(cmd)
    else:
        log("Could not find file before imgconvert_cmd, aborted")

    if (copy_last and os.path.exists(fileName)):
        copyfile(fileName, status_filename)
    else:
        log("Aborted copying of file")


capture()
