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
from logger import log, silentlog, redText, greenText, getTime, loglastfile
import locale
import subprocess as sp
from localStoragePy import localStoragePy
from virtualTimer import getCurrentExposure
import pytz



### Define variables
v = '0.2.2'
time_start = datetime.now()
camera = PiCamera()
this_executable = os.path.basename(__file__)
homedir = sys.path[0]
total_images = 0
localStorage = localStoragePy('ekstremedia-timelapse-exposure', 'sqlite')
js = os.path.join(homedir, "data/solartimes.json")
python_version = sys.version





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
    if config['resolution']:
        camera.resolution = (
            config['resolution']['width'],
            config['resolution']['height']
        )
        
    try:
        camera_name = config['camera_name']
    except KeyError:
        camera_name = "RaspberryTimelapse"

    try:
        max_exposure = config['max_exposure']
    except KeyError:
        max_exposure = 6000000

    try:
        min_exposure = config['min_exposure']
    except KeyError:
        min_exposure = 6000000

    try:
        exposure_ratio = config['exposure_ratio']
    except KeyError:
        exposure_ratio = 30000

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
    try:
        status_filename = config['status_filename']
    except KeyError:
        status_filename = False
    try:
        copy_last = config['copy_last']
    except KeyError:
        copy_last = False









def start():
    log(f'{redText("Raspberry")} {greenText("Pi")} v{v} timelapse is loading')
    log(f'Running on python {greenText(python_version[0:6])}')
    log(f'Camera name: {greenText(camera_name)}')
    log(f'Images saved to: {greenText(file_path)} with prefix {greenText(file_prefix)}.')
    log(f'White balance: {greenText(white_balance)}, gains: {greenText(str(awb_gains[0]))},{greenText(str(awb_gains[1]))}.')
    log(f'Interval: every {greenText(str(interval))} second')
    log(f'Exposure max / min: {greenText(str(max_exposure))} / {greenText(str(min_exposure))} microseconds')
    camera.awb_mode = white_balance
    camera.awb_gains = awb_gains
    camera.framerate = Fraction(1, 6)
    while not sleep(interval):
        capture()




def capture():
   
    global max_exposure
    global min_exposure
    time_now = datetime.now()
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

    log(f"Sunrise, sunset:           {greenText(getTime(sunrise_today))} / {greenText(getTime(sunset_today))}.")
    log(f"Time to start / end day:   {greenText(getTime(timeToStartDay))} / {greenText(getTime(timeToEndDay))}")
    log(f"End of day:                {greenText(getTime(endOfDay))}")
    
    if (time_now > sunrise_today and time_now < sunset_today):
        isDay = True
    else:
        isDay = False

    isDay = True
    log(f"Is day: {isDay}")

    if isDay:
        global copy_last
        global total_images
        global status_filename

        log("Setting daytime variables")
        log(greenText('DAYTIME'))
        camera.iso = 60
        camera.shutter_speed = 0
        log(f"Shutter speed: {camera.shutter_speed}, iso: {camera.iso}")
        today = os.path.join(file_path, str(time_now.year), str(
            '%02d' % time_now.month), str('%02d' % time_now.day))
        time = str('%02d' % time_now.hour)+"_"+str('%02d' % time_now.minute)+"_"+str('%02d' % time_now.second)
        date = str('%02d' % time_now.day)+"_"+str('%02d' % time_now.month)+"_"+str('%02d' % time_now.year)
        if not os.path.exists(today):
            os.makedirs(today)
            log("Created folder: " + greenText(today))
        fileName = os.path.join(today+"/"+file_prefix+"-"+date+"_"+time+".jpg")
        sleep(10)
        localStorage.setItem('currentExposure', camera.shutter_speed)
        log("Capturing image...")
        camera.capture(fileName)

        total_images = total_images+1
        log(f"Captured: {greenText(fileName)} #{greenText(str(total_images))}")
        loglastfile(fileName)

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
        log("Pausing camera...")




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
                getExposure = getExposure-exposure_ratio
                if (getExposure < min_exposure):
                    getExposure = min_exposure
            else:
                getExposure = min_exposure
                camera.shutter_speed = 0
        elif (time_now > timeToEndDay or time_now < timeToStartDay):
            log("Getting into darkness..")
            if (getExposure < max_exposure):
                getExposure = getExposure+exposure_ratio
                if (getExposure > max_exposure):
                    getExposure = max_exposure
        
        log(f"Setting exposure: {greenText(str(getExposure))}")
        camera.shutter_speed = getExposure
        # camera.shutter_speed = getExposure
        
        if (getExposure>5000000):
            camera.iso = 800
        else:
            camera.iso = 60
        
    
        log(f"Camera settings: ISO: {greenText(str(camera.iso))}, shutter speed: {greenText(str(camera.shutter_speed))}")

        ## Take photo
        # sleep(10)
        # today = str('%02d' % now.day) + "." + str('%02d' % now.month) + " " + str(now.year) + "  "
        # timeprint = today + str('%02d' % now.hour) + ":" + str('%02d' % now.minute) 


        today = os.path.join(file_path, str(time_now.year), str(
            '%02d' % time_now.month), str('%02d' % time_now.day))
        time = str('%02d' % time_now.hour)+"_"+str('%02d' % time_now.minute)+"_"+str('%02d' % time_now.second)
        date = str('%02d' % time_now.day)+"_"+str('%02d' % time_now.month)+"_"+str('%02d' % time_now.year)
        if not os.path.exists(today):
            os.makedirs(today)
            log("Created folder: " + greenText(today))
        fileName = os.path.join(today+"/"+file_prefix+"-"+date+"_"+time+".jpg")
        sleep(10)
        localStorage.setItem('currentExposure', camera.shutter_speed)
        log("Capturing image...")
        camera.capture(fileName)

        # global copy_last
        # global total_images
        # global status_filename
        total_images = total_images+1
        log(f"Captured: {greenText(fileName)} #{greenText(str(total_images))}")
        loglastfile(fileName)

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
        log("Pausing camera...")
        # camera.close()

start()
