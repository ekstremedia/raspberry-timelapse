#!/usr/bin/env /usr/local/bin/python3.9

from logger import *
import datetime
import locale
import calendar
from calendar import weekday, day_name
import yaml
import os
from os import path
import sys
import subprocess as sp
import ffmpeg

print(" ")
log(f"tl.py {greenText('started')}")

# Initialize
locale.setlocale(locale.LC_ALL, "nb_NO")
config = yaml.safe_load(open(os.path.join(sys.path[0], "config.yml")))

try:
    camera_name = config['annotation']
except KeyError:
    camera_name = "Timelapse"

try:
    filePrefix = config['filePrefix']
except KeyError:
    filePrefix = "timelapse"

# Set date variables

# Yesterdays date
previous_date = datetime.datetime.today() - datetime.timedelta(days=1)

# set a specific date instead
#previous_date = date.fromisoformat('2021-01-24') 

previous_datestr = previous_date.strftime ('%Y/%m/%d');
#previous_datestr_out = previous_date.strftime ('%Y-%m-%d');
previous_filename = previous_date.strftime ('%d_%m_%Y');
previous_day = previous_date.strftime ('%d');                               # 05
previous_month = previous_date.strftime ('%m');                             # 01
previous_year = previous_date.strftime ('%Y');                              # 2021
day = previous_date.strftime ('%-d')                                        # 5
month = previous_date.strftime ('%-m')                                      # 1
year = previous_year
dayNumber = weekday(int(year), int(month), int(day))
pretty_month = calendar.month_name[int(month)]
pretty_day = calendar.day_name[int(dayNumber)]
pretty_date = f"{pretty_day} {day}. {pretty_month} {year}".capitalize()

log(f"Yesterdays date: {greenText(pretty_date)} ({previous_datestr})")

# Set image and video variables
images_folder = '/var/www/html/bilder'
video_folder = os.path.join('/var/www/html/videoer', previous_year, previous_month)+"/"
video_file = video_folder+filePrefix+"_"+previous_filename+".mp4" # TODO: add cameraname to filename
target = os.path.join(images_folder, previous_datestr)+"/"
extension = '*.jpg'

log(f"Target folder: {greenText(target)}")

# Create videofolder if not exists
if not os.path.exists(video_folder):
    os.makedirs(video_folder)
    log("Created folder: "+ greenText(video_folder))

# Look for overexposed images, files lower than 100k
overexposed_cmd = f"find {target+extension} -type f -size -100k | wc -l"
#overdelete = f"find {target+extension} -type f -size -100k -delete"
restfiles_cmd = f"find {target+extension} -type f | wc -l"
overexposed_count = sp.getoutput(overexposed_cmd)
#if int(overexposed_count)>0:
#    log(f"Deleting {redText(overexposed_count)} overexposed images in {greenText(target)}...")
#    delete = sp.getoutput(overdelete)
#    log("Deleted.")
#else:
    #log("No overexposed images found")
restfiles = sp.getoutput(restfiles_cmd)

# FFMPEG
ffmpeg_cmd = f"ffmpeg -r 25 -pattern_type glob -i '{target+extension}' -crf 23 -c:v libx264 -vstats_file /home/pi/raspberry-timelapse/logs/ffmpeg.log -y {video_file}"
log(ffmpeg_cmd)
log(f"Running ffmpeg on {greenText(restfiles)} images...")
ffmpg_call = sp.getoutput(ffmpeg_cmd)
size = round(os.path.getsize(video_file)/(1024*1024),2)

if path.exists(video_file) and size>0:
    log(f"Successfully created {greenText(video_file)} {size} MB")
    
else:
    log(f"Error in creating video file: {video_file}: {size} MB")

title = f"{camera_name} - {pretty_date.capitalize()}"
yt_cmd = f"/home/pi/raspberry-timelapse/youtubeUpload.py --file='{video_file}' --title='{title}' --description='Automagisk laget på en Raspberry Pi 3b+' --keywords='timelapse, vesterålen, {pretty_date}' --category='1' --privacyStatus='public'"
log(yt_cmd)
cmd_output = sp.getoutput(yt_cmd)
log("Ran: "+cmd_output)
