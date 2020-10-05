#!/usr/bin/env python3
from time import sleep
from datetime import datetime, date, time
from colorama import init, Fore, Back, Style
# from picamera import PiCamera
from fractions import Fraction
import emoji
import yaml
import os
import sys
from picamera import PiCamera

config_file = "config_testshot.yml"

init()

currentDir = os.getcwd()


def timeNow():
    now = datetime.now()
    return str('%02d' % now.hour) + ":" + str('%02d' % now.minute) + ":" + str('%02d' % now.second)


def timeNowFn():
    now = datetime.now()
    return str('%02d' % now.hour) + "_" + str('%02d' % now.minute) + "_" + str('%02d' % now.second)


def dateTimeNowFn():
    now = datetime.now()
    date = f"{'%02d' % now.day }.{'%02d' % now.month}.{'%02d' % now.year}"
    return date+str('-%02d' % now.hour) + "_" + str('%02d' % now.minute) + "_" + str('%02d' % now.second)


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
    config = yaml.safe_load(open(os.path.join(sys.path[0], config_file)))
    loadedConf = True
    infoMsg("Loading config file "+Fore.GREEN+config_file+Fore.RESET+".")
except OSError as e:
    infoMsg(Fore.RED+"Found no configuration file!"+Fore.RESET)
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
        awbg = config['white_balance_gain']
    except KeyError:
        awbg = ''
    infoMsg("White balance gain: "+greenText(awbg))

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

tmpFileName = filePath+filePrefix+"_"+dateTimeNowFn() + "_iso-"+str(iso)+"_shutter-"+str(shutter_speed)+"_meter-" + \
    str(metering)+"_exposuremode-"+str(exposure_mode) + \
    "_int-"+str(interval)+"_awb-"+str(awb)+"_awbg-" + \
    str(awbg['red_gain'])+"_"+str(awbg['blue_gain'])+".jpg"

infoMsg(tmpFileName)


def set_camera_options(camera):
    if config['metering']:
        camera.meter_mode = config['metering']

    if config['resolution']:
        camera.resolution = (
            config['resolution']['width'],
            config['resolution']['height']
        )

    if config['framerate']:
        camera.framerate = Fraction(1, 6)

    if config['iso']:
        camera.iso = config['iso']

    if config['shutter_speed']:
        camera.shutter_speed = config['shutter_speed']

    if config['white_balance']:
        camera.awb_mode = config['white_balance']

    if config['white_balance_gain']:
        camera.awb_gains = (
            config['white_balance_gain']['red_gain'],
            config['white_balance_gain']['blue_gain']
        )

    if config['exposure_mode']:
        camera.exposure_mode = config['exposure_mode']

    sleep(5)
    # infoMsg("Camera ready, starting!")

    return camera


def take(fileName):

    if not os.path.exists(filePath):
        os.makedirs(filePath)
        infoMsg("Created folder: " + greenText(filePath))
    camera = PiCamera()
    set_camera_options(camera)
    infoMsg("Capturing...")
    camera.annotate_text = tmpFileName
    camera.annotate_text_size = 12
    camera.capture(tmpFileName)
    infoMsg('Captured ' + tmpFileName)
    camera.close()


take(tmpFileName)
