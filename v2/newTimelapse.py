#!/usr/bin/env /usr/bin/python3.7
from time import sleep
from datetime import datetime, date, time, timedelta
# from picamera import PiCamera
from fractions import Fraction
from shutil import copyfile
import os
import threading
import sys
import yaml
import json
from logger import log, silentlog, redText, greenText, getTime
import locale
import subprocess as sp
from localStoragePy import localStoragePy
from virtualTimer import getCurrentExposure
import pytz

# Define variables
this_executable = os.path.basename(__file__)
v = '0.2.1'
total_images = 0
homedir = sys.path[0]
localStorage = localStoragePy('ekstremedia-timelapse-exposure', 'sqlite')
js = os.path.join(homedir, "data/solartimes.json")
tz = pytz.timezone('Europe/Oslo')
python_version = sys.version
log(f'{redText("Raspberry")} {greenText("Pi")} v{v} timelapse is loading')
log(f'Running on python {greenText(python_version[0:6])}')


# Get config values
try:
    config = yaml.safe_load(open(os.path.join(homedir, "config.yml")))
    loadedConf = True
    log(f'Configuration {greenText("loaded")}.')
except OSError as e:
    log(f"{redText('Found no configuration file!')}")
    log(f"{redText('Edit example.config.yml and save it as config.yml and restart')} {greenText(this_executable)}.")
    # log(str(e))
    loadedConf = False
    quit()

if loadedConf:
    try:
        camera_name = config['camera_name']
    except KeyError:
        camera_name = "RaspberryTimelapse"

    try:
        max_exposure = config['max_shutter_speed']
    except KeyError:
        max_exposure = 6000000

    try:
        file_path = config['filePath']
    except KeyError:
        file_path = currentDir+"/timelapse/"

    try:
        file_prefix = config['filePrefix']
    except KeyError:
        file_prefix = "tl"

    if config['white_balance']:
        white_balance = config['white_balance']
    else:
        white_balance = 'cloudy'

    if config['white_balance_gain']:
        awb_gains = (
            config['white_balance_gain']['red_gain'],
            config['white_balance_gain']['blue_gain']
        )
    else:
        # Set fixed awb gains to avoid flickering
        awb_gains = (
            1.6,
            1.7
        )
    try:
        interval = config['interval']
    except KeyError:
        interval = 10

log(f'Camera name: {greenText(camera_name)}')
log(f'Images saved to: {greenText(file_path)}')
log(f'File name prefix: {greenText(file_prefix)}')
log(f'White balance: {greenText(white_balance)}')
log(f'Interval: every {greenText(str(interval))} second')
log(f'Maximum exposure: {greenText(str(max_exposure))} microseconds')
# log(f'awb_gains: {greenText(awb_gains["red_gain"])}')


def set_capture_variables():
    global max_exposure
    mytz = datetime.now()
    # mytz = tz.localize(mytz)
    # print(f"mytz: {mytz}")
    day = mytz.strftime('%d')                               # 05
    month = mytz.strftime('%m')
    dateStr = day+"-"+month
    with open(js) as json_file:
        solardata = json.load(json_file)
        day = solardata[dateStr]
        if not day['data']:
            polar = True
            polarType = day['sun']
        else:
            polar = False
            sunrise = day['sunrise']
            sunset = day['sunset']
    # print(f"Mytz: {mytz}")

    if not polar: 
        sunriseHour = int(sunrise[0:2])
        sunriseMinute = int(sunrise[3:5])
        sunsetHour = int(sunset[0:2])
        sunsetMinute = int(sunset[3:5])
    else:
        # print(f"Polar time, sun: {polarType}")
        if (polarType == 'never_sets'):
            sunriseHour = 9
            sunriseMinute = 00
            sunsetHour = 12
            sunsetMinute = 00
            max_exposure = 10000
            min_exposure = 2000
        if (polarType == 'never_rises'):
            sunriseHour = 22
            sunriseMinute = 00
            sunsetHour = 23
            sunsetMinute = 00
            max_exposure = max_exposure
            min_exposure = 2000
    sunrise_today = mytz.replace(hour=sunriseHour,minute=sunriseMinute, second=0, microsecond=0)
    sunset_today = mytz.replace(hour=sunsetHour,minute=sunsetMinute, second=0, microsecond=0)
    timeToStartDay = sunrise_today - timedelta(minutes=180)
    endOfDay = sunset_today + timedelta(minutes=135)
    timeToEndDay = sunset_today + timedelta(minutes=20)

    log(f"Sunrise, sunset: {getTime(sunrise_today)} - {getTime(sunset_today)}")
    log(f"Time to start day: {getTime(timeToStartDay)}")
    log(f"Time to end day: {getTime(timeToEndDay)}")
    log(f"End of day: {getTime(endOfDay)}")

    if (mytz < timeToStartDay or mytz > endOfDay):
        currentExposure = max_exposure
    else:
        getExposure = localStorage.getItem('currentExposure')
        if (str(getExposure) == 'None'):
            if (mytz < timeToStartDay or mytz > endOfDay):
                # print(f"None set, defaulting to {max_exposure}")
                localStorage.setItem('currentExposure', max_exposure)
                currentExposure = max_exposure
            elif(mytz>= timeToStartDay and mytz <= endOfDay):
                # print(f"None set, defaulting to {default_exposure}")
                localStorage.setItem('currentExposure', default_exposure)
                currentExposure = default_exposure
        # else:

        if (str(getExposure) != 'None'):        
            currentExposure = int(getExposure)

            # print(currentExposure)
    if (mytz > timeToStartDay and mytz < timeToEndDay):
        # print(currentExposure)
        if (currentExposure > min_exposure):
            currentExposure = currentExposure-exposureRatio
            if (currentExposure < min_exposure):
                currentExposure = min_exposure
        else:
            currentExposure = min_exposure
    elif (mytz > timeToStartDay and mytz > timeToEndDay):
        if (currentExposure < max_exposure):
            currentExposure = currentExposure+exposureRatio
            if (currentExposure > max_exposure):
                currentExposure = max_exposure

    localStorage.setItem('currentExposure', currentExposure)

def take(fileName):
    # camera = PiCamera()
    # set_camera_options(camera)
    # Capture a picture.
    log("")
    log("Capturing...")
    now = datetime.now()
    date_day = str('%02d' % now.day)
    date_month = str('%02d' % now.month)
    date_year = str(now.year)
    date_hour = str('%02d' % now.hour)
    date_minute = str('%02d' % now.minute) 
    date_second = str('%02d' % now.second)
    
    image_name = f"{file_prefix}-{date_day}_{date_month}_{date_year}-{date_hour}_{date_minute}_{date_second}.jpg"

    global total_images
    total_images += 1

    shutter_speed = getCurrentExposure()
    log(str(image_name))
    log(str(shutter_speed))
    set_capture_variables()

take('test')
