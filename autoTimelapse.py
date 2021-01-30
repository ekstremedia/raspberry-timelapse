#!/usr/bin/env python3.9

import datetime
import subprocess as sp
import os
from datetime import date

Previous_Date = datetime.datetime.today() - datetime.timedelta(days=1)
#Previous_Date = datetime.datetime(2021,4,25)
#Previous_Date = date.fromisoformat('2019-12-04')

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

print(target)

tl_cmd = f"/home/pi/raspberry-timelapse/makeTimelapse.py {target} {video_file} {previous_datestr_out}"
print(tl_cmd)

sp.call(tl_cmd, shell=True)