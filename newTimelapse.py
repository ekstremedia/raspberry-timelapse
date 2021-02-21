#!/usr/bin/env /usr/local/bin/python3.9
from time import sleep
from datetime import datetime, date, time
# from picamera import PiCamera
from fractions import Fraction
from shutil import copyfile
import os
import threading
import sys
import yaml
from logger import log, silentlog, redText, greenText
import locale
import subprocess as sp
from localStoragePy import localStoragePy
from virtualTimer import getCurrentExposure

log(redText("Raspberry")+greenText("Pi")+"-timelapse is loading")
