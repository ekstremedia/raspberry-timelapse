#!/usr/bin/env python3.9

import datetime
import subprocess as sp
import os
from datetime import date
import sys
import logging

Previous_Date = datetime.datetime.today() - datetime.timedelta(days=1)
#Previous_Date = datetime.datetime(2021,4,25)
#Previous_Date = date.fromisoformat('2019-12-04')


# Initialize logging
homedir = sys.path[0]
logdir = os.path.join(homedir, "logs")
logfilename = "makeTimelapse.log"
logfile = os.path.join(logdir, logfilename)
if not os.path.exists(logdir):
    os.makedirs(logdir)
    print("Made logs/ directory")
logging.basicConfig(filename=logfile, encoding="utf-8", level=logging.DEBUG)
def log(text):
    now = datetime.datetime.now()
    today = str('%02d' % now.day) + "." + str('%02d' % now.month) + "." + str(now.year) + " "
    timeprint = today + str('%02d' % now.hour) + ":" + str('%02d' % now.minute) + ":" + str('%02d' % now.second)
    dateStr = timeprint + ": "
    logging.info(dateStr + text)
log("Started autotimelapse")

print (Previous_Date)
previous_datestr = Previous_Date.strftime ('%Y/%m/%d');
previous_datestr_out = Previous_Date.strftime ('%Y-%m-%d');
previous_filename = Previous_Date.strftime ('%d_%m_%Y');
previous_month = Previous_Date.strftime ('%m');
previous_year = Previous_Date.strftime ('%Y');
previous_day = Previous_Date.strftime ('%d');


images_folder = '/var/www/html/bilder'
video_folder = os.path.join('/var/www/html/videoer', previous_year, previous_month)+"/"
print(f"Video folder: {video_folder}")

video_file = video_folder+previous_filename+".mp4"
print(f"Video file: {video_file}")

if not os.path.exists(video_folder):
    os.makedirs(video_folder)

target = os.path.join(images_folder, previous_datestr)+"/"
log(target)
tl_cmd = f"/home/pi/raspberry-timelapse/makeTimelapse.py {target} {video_file} {previous_datestr_out}"
log(tl_cmd)
#sp.call(tl_cmd, shell=True)
os.system(tl_cmd)
