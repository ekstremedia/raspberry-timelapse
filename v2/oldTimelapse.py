#!/usr/bin/env /usr/bin/python3.7
from time import sleep
from datetime import datetime, date, time, timedelta
from picamera import PiCamera
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
time_start = datetime.now()
camera = PiCamera()
this_executable = os.path.basename(__file__)
v = '0.2.1'
total_images = 0
homedir = sys.path[0]
localStorage = localStoragePy('ekstremedia-timelapse-exposure', 'sqlite')
js = os.path.join(homedir, "data/solartimes.json")
tz = pytz.timezone('Europe/Oslo')
python_version = sys.version
exposureRatio = 30390
min_exposure = 2000



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
        file_path = config['file_path']
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

# Set initial camera settings
camera.awb_mode = white_balance
camera.awb_gains = awb_gains



def set_capture_variables():
    global max_exposure
    global min_exposure
    time_now = time_start
    # time_now = datetime.now()

    # time_now = tz.localize(time_now)
    # print(f"time_now: {time_now}")
    day = time_now.strftime('%d')                               # 05
    month = time_now.strftime('%m')
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
    # print(f"time_now: {time_now}")

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
    sunrise_today = time_now.replace(hour=sunriseHour,minute=sunriseMinute, second=0, microsecond=0)
    sunset_today = time_now.replace(hour=sunsetHour,minute=sunsetMinute, second=0, microsecond=0)
    timeToStartDay = sunrise_today - timedelta(minutes=180)
    endOfDay = sunset_today + timedelta(minutes=135)
    timeToEndDay = sunset_today + timedelta(minutes=20)

    log(f"Sunrise, sunset: {getTime(sunrise_today)} - {getTime(sunset_today)}")
    log(f"Time to start day: {getTime(timeToStartDay)}")
    log(f"Time to end day: {getTime(timeToEndDay)}")
    log(f"End of day: {getTime(endOfDay)}")
    
    if (time_now > sunrise_today and time_now < sunset_today):
        isDay = True
    else:
        isDay = False

    log(f"Is day: {isDay}")

    if isDay:
        log("Setting daytime variables")
        log(greenText('DAYTIME'))
        camera.iso = 60
        camera.shutter_speed = 0
        log(f"Shutter speed: {camera.shutter_speed}, iso: {camera.iso}")
    if not isDay:
        log("Setting nighttime variables")
        getExposure = int(localStorage.getItem('currentExposure'))
        if (str(getExposure) == 'None'):
            log(f"Exposure not set, setting to 2000")
            getExposure = 2000
            localStorage.setItem('currentExposure', getExposure)
        else: 
            log(f"Got Exposure: {getExposure}")

        if (time_now > timeToStartDay and time_now < timeToEndDay):
            # print(currentExposure)
            if (getExposure > min_exposure):
                getExposure = getExposure-exposureRatio
                if (getExposure < min_exposure):
                    getExposure = min_exposure
            else:
                getExposure = min_exposure
        elif (time_now > timeToEndDay or time_now < timeToStartDay):
            log("Getting into darkness..")
            if (getExposure < max_exposure):
                getExposure = getExposure+exposureRatio
                if (getExposure > max_exposure):
                    getExposure = max_exposure
        log(f"New exposure: {getExposure}")
        localStorage.setItem('currentExposure', getExposure)
        camera.shutter_speed = getExposure
        if (getExposure>5000000):
            camera.iso = 800

def take(fileName):
    # set_camera_options(camera)
    # Capture a picture.
    # log()
    log("Capturing...")
    # now = datetime.now()
    now = time_start
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




def capture():
    set_capture_variables()
    if not os.path.exists(file_path):
        os.makedirs(file_path)
        log("Created folder: " + greenText(file_path))

    log("Set timelapse-folder to: "+greenText(file_path))
    log("")
    log("Starting timelapse in "+greenText(str(interval)) + " ... :) ")
    log("Shutter: " + greenText(str(shutter_speed)) + " microseconds, ISO: " + greenText(str(iso)) + ", taking photo every " + greenText(
        str(interval)) + " seconds")
    now = datetime.now()
    today = os.path.join(file_path, str(now.year), str(
        '%02d' % now.month), str('%02d' % now.day))
    time = str('%02d' % now.hour) + "_" + str('%02d' %
                                                now.minute) + "_" + str('%02d' % now.second)
    timePrint = str('%02d' % now.hour) + ":" + str('%02d' %
                                                    now.minute) + ":" + str('%02d' % now.second)
    if not os.path.exists(today):
        os.makedirs(today)
        log("Created folder: " + greenText(today))
    fileName = os.path.join(today + "/" + filePrefix + "_" + time + ".jpg")
#    take(fileName)

    while not sleep(interval):
        # Date and time settings
        now = datetime.now()
        today = os.path.join(file_path, str(now.year), str(
            '%02d' % now.month), str('%02d' % now.day))
        time = str('%02d' % now.hour)+"_"+str('%02d' %
                                                now.minute)+"_"+str('%02d' % now.second)
        if not os.path.exists(today):
            os.makedirs(today)
            log("Created folder: " + greenText(today))
        fileName = os.path.join(today+"/"+filePrefix+"_"+time+".jpg")
        take(fileName)













# take('test')

# time_start = datetime(2021,2,5,7,4)
# for i in range(2000):
#     time_start = time_start + timedelta(minutes=1)
#     log(f"TimeStart: {greenText(getTime(time_start))}")
       
#     hr = time_start.strftime('%H:%M')
#     # ps = f"Time: {hr}, ex: {ex}"
#     set_capture_variables()
    