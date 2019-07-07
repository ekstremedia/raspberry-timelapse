#!/usr/bin/env python3
from datetime import datetime, date, time
from picamera import PiCamera
import os
import time
import sys
import yaml
config = yaml.safe_load(open(os.path.join(sys.path[0], "config.yml")))
def set_camera_options(camera):
    # Set camera resolution.

    
    if config['resolution']:
        camera.resolution = (
            config['resolution']['width'],
            config['resolution']['height']
        )
    camera.iso = 100

    if config['isloaded']:
        print("Configuration file loaded!")
    else:
        print("Configuration file not loaded!")

camera = PiCamera()
set_camera_options(camera)

print(camera.iso)
#rint dir(camera)









