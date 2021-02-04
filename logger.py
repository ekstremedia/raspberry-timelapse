#!/usr/bin/env /usr/local/bin/python3.9
import sys
import os 
import logging
from datetime import datetime, date, time

# Initialize logging
homedir = sys.path[0]
logdir = os.path.join(homedir, "logs")
logfilename = "tl.log"
last_image = "last_image.log"
last_shutter = "last_shutter.log"
logfile = os.path.join(logdir, logfilename)
last_image_file = os.path.join(logdir, last_image)
last_shutter_file = os.path.join(logdir, last_shutter)
red = "\033[1;31;38m"
green = "\033[1;32;38m"
endcolor = "\033[0m"

if not os.path.exists(logdir):
    os.makedirs(logdir)
    print("Made logs/ directory")

logging.basicConfig(filename=logfile, encoding="utf-8", level=logging.DEBUG)


def redText(text):
    return red+text+endcolor


def greenText(text):
    return green+text+endcolor


def errorMsg(text):
    print(red+text+endcolor)


def successMsg(text):
    print(green+text+endcolor)

def log(text):
    now = datetime.now()
    today = str('%02d' % now.day) + "." + str('%02d' % now.month) + "." + str(now.year) + " "
    timeprint = today + str('%02d' % now.hour) + ":" + str('%02d' % now.minute) + ":" + str('%02d' % now.second)
    timePrint = str('%02d' % now.hour) + ":" + str('%02d' % now.minute) + ":" + str('%02d' % now.second)
    logText = greenText("[") + timePrint + greenText("]") + " " + text
    logging.info(logText)
    print(logText)

def loglastfile(filename):
    f = open(last_image_file, "w+")
    f.write(f"{filename}")
    f.close()

def logLastShutterSpeed(shutterspeed):
    f = open(last_shutter_file, "w+")
    f.write(f"{shutterspeed}")
    f.close()