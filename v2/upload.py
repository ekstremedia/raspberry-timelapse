#!/usr/bin/env /usr/bin/python3.7
from logger import log, silentlog, redText, greenText, getTime, loglastfile
import subprocess as sp
import yaml
import os
import sys
import datetime
from localStoragePy import localStoragePy


homedir = sys.path[0]
python_version = sys.version[0:6]
localStorage = localStoragePy('ekstremedia-timelapse-exposure', 'sqlite')
output_date = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%SZ")

# Get data from config file
try:
    config = yaml.safe_load(open(os.path.join(homedir, "config.yml")))
    loadedConf = True
except OSError as e:
    log(f"{redText('Found no configuration file!')}")
    log(f"{redText('Edit example.config.yml and save it as config.yml and restart')} {greenText(this_executable)}.")
    # log(str(e))
    loadedConf = False
    quit()
try:
    camera_name = config['camera_name']
except KeyError:
    camera_name = "RaspberryTimelapse"
try:
    raspberry = config['raspberry_version']
except KeyError:
    raspberry = "Raspberry Pi 3B+"

raspberry = sp.getoutput('cat /proc/device-tree/model')
osinfo = sp.getoutput('lsb_release -irdc')
uname = sp.getoutput('uname -a')
uptime = sp.getoutput('uptime')

last_video_filename = localStorage.getItem('last_video_filename')
last_video_filesize = localStorage.getItem('last_video_filesize')
last_video_picture_count = localStorage.getItem('last_video_picture_count')
tags = f"sortland, vesterålen, raspberry, timelapse, {raspberry}, picamera, raspbian, raspistill"

description = f"Automagisk laget på en {raspberry}\n\nOperativsystem: {osinfo}\n\n{uname}\n\n{uptime}\n\nPython: {python_version} \n\nFilename: {last_video_filename} ({last_video_filesize} mb) from {last_video_picture_count} pictures"

yt_cmd = f"python3.7 /home/pi/raspberry-timelapse/v2/youtube-upload-master/youtube_upload/ --title='{camera_name}' --description='{description}'  {last_video_filename}"
log(yt_cmd)
p = sp.getoutput(yt_cmd)
log(p)
# run_cmd = sp.getoutput(yt_cmd)
# sp.Popen(yt_cmd)

# print(run_cmd)
