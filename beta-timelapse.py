#!/usr/bin/env python3
from time import sleep
from datetime import datetime, date, time
from colorama import init, Fore, Back, Style
#from picamera import PiCamera
import emoji
import yaml
import os
import sys

init()

currentDir = os.getcwd()


def timeNow():
    now = datetime.now()
    return str('%02d' % now.hour) + ":" + str('%02d' % now.minute) + ":" + str('%02d' % now.second)
print(timeNow())
def infoMsg(text):
    print(Fore.BLUE+"ℹ"+Fore.RESET + Fore.GREEN +
          (" ["+timeNow()+'] ')+Fore.RESET+text)

def greenText(text):
     return Fore.GREEN+str(text)+Fore.RESET

def redText(text):
     return Fore.RED+text+Fore.RESET

infoMsg(Fore.RED+"Raspberry"+Fore.RESET+Fore.GREEN +
        "PI"+Fore.RESET+"-timelapse "+emoji.emojize(":camera:")+" is loading...")
infoMsg("Made by Terje Nesthus ("+Fore.LIGHTBLUE_EX+"terje"+Fore.RESET +
        Fore.BLUE+"@"+Fore.RESET+Fore.LIGHTBLUE_EX+"nesthus.no"+Fore.RESET+")")

# Load configuration
try:
    config = yaml.safe_load(open(os.path.join(sys.path[0], "beta_config.yml")))
    loadedConf = True
except OSError as e:
    infoMsg("Found no configuration file!")
    infoMsg(str(e))
    loadedConf = False

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
    infoMsg("ISO: "+greenText(iso))

    try:
        awb = config['white_balance']
    except KeyError:
        awb = 'cloudy'
    infoMsg("White balance: "+greenText(awb))

    try:
        interval = config['interval']
    except KeyError:
        interval = 10
    infoMsg("Interval time: "+greenText(interval))

    try:
        shutter_speed = config['shutter_speed']
    except KeyError:
        shutter_speed = 0
    infoMsg("Shutter speed: "+greenText(shutter_speed))

    try:
        metering = config['metering']
    except KeyError:
        metering = None
    infoMsg("Metering: "+greenText(metering))

    try:
        exposure_mode = config['exposure_mode']
    except KeyError:
        exposure_mode = None
    infoMsg("Exposure mode: "+greenText(exposure_mode))

    try:
        copy_last = config['copy_last']
    except KeyError:
        copy_last = False
    infoMsg("Copy captured image: "+greenText(copy_last))

    try:
        status_filename = config['status_filename']
    except KeyError:
        status_filename = False
    infoMsg("Copy to: "+greenText(status_filename))

