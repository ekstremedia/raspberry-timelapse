#!/usr/bin/env /usr/local/bin/python3.9
import subprocess as sp
# temp  = sp.getoutput('/opt/vc/bin/vcgencmd measure_temp')
temp  = sp.getoutput('cat /sys/class/thermal/thermal_zone0/temp')
tempC = round(int(temp)/1000,1)
print(tempC)
# print(temp[5:-2]) 