#!/usr/bin/env python3.9
import yaml
import locale
import calendar
from calendar import weekday, day_name
import sys
import os
import subprocess as sp
import logging
from datetime import datetime, date, time
locale.setlocale(locale.LC_ALL, "nb_NO")

config = yaml.safe_load(open(os.path.join(sys.path[0], "config.yml")))
try:
    camera_name = config['annotation']
except KeyError:
    camera_name = ""


# Initialize variables
target_folder = sys.argv[1]
output_filename = sys.argv[2]
date = date.fromisoformat(sys.argv[3])
month = date.strftime ('%-m')
year = date.strftime ('%Y')
day = date.strftime ('%-d')
dayNumber = weekday(int(year), int(month), int(day))

pretty_month = calendar.month_name[int(month)]
pretty_day = calendar.day_name[int(dayNumber)]

pretty_date = f"{pretty_day} {day}. {pretty_month} {year}"

title = f"{camera_name} - {pretty_date.capitalize()}"

print(pretty_date)

extension = '*.jpg'
homedir = sys.path[0]

# Initialize logging
logdir = os.path.join(homedir, "logs")
logfilename = "makeTimelapse.log"
logfile = os.path.join(logdir, logfilename)
if not os.path.exists(logdir):
    os.makedirs(logdir)
    print("Made logs/ directory")
logging.basicConfig(filename=logfile, encoding="utf-8", level=logging.DEBUG)
def log(text):
    now = datetime.now()
    today = str('%02d' % now.day) + "." + str('%02d' % now.month) + "." + str(now.year) + " "
    timeprint = today + str('%02d' % now.hour) + ":" + str('%02d' % now.minute) + ":" + str('%02d' % now.second)
    dateStr = timeprint + ": "
    logging.info(dateStr + text)
log("Started maketimelapse")
log(f"Looking for: {target_folder+extension}")
log(f"Outputting to: {output_filename}")
over = f"find {target_folder+extension} -type f -size -100k | wc -l"
overdelete = f"find {target_folder+extension} -type f -size -100k -delete"
overexposed = sp.getoutput(over)
if int(overexposed)>0:
    log(f"Deleting {overexposed} overexposed images...")
    log(f"Deleting {overexposed} overexposed images in {target_folder}")
    delete = sp.getoutput(overdelete)
else:
    log("No overexposed images found")

ffmpeg_cmd = f"ffmpeg -r 25 -pattern_type glob -i '{target_folder+extension}' -c:v libx264 -y {output_filename}"
log(ffmpeg_cmd)
sp.call(ffmpeg_cmd, shell="True")
log(ffmpeg_cmd)
log(output_filename)

# --noauth_local_webserver
yt_cmd = f"/home/pi/raspberry-timelapse/youtubeUpload.py --file='{output_filename}' --title='{title}' --description='Automagisk laget på en Raspberry Pi 3b+' --keywords='timelapse, vesterålen, {pretty_date}' --category='22' --privacyStatus='public'"
log(yt_cmd)
#sp.call(yt_cmd, shell=True)
cmd_output = sp.getoutput(yt_cmd)
log("Ran: "+cmd_output)
