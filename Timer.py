#!/usr/bin/env /usr/local/bin/python3.9
import pytz
import json
from datetime import datetime, time, timezone, timedelta
import os
import sys
from localStoragePy import localStoragePy

localStorage = localStoragePy('ekstremedia-timelapse-exposure', 'sqlite')
tz = pytz.timezone('Europe/Oslo')
#mytz = datetime(2021,2,5,8,11);
mytz = datetime.now()
mytz = tz.localize(mytz)
# print(f"mytz: {mytz}")
day = mytz.strftime('%d')                               # 05
month = mytz.strftime('%m')
dateStr = day+"-"+month
hour = mytz.strftime('%H:%M')                               # 05
# print(f"Now: {mytz}")
# print(f"Hour {hour}")
exposure_max = 6000000
localStorage.setItem('exposure', exposure_max)
exposure_min = 4000
js = os.path.join(sys.path[0], "scripts/solartimes.json")
with open(js) as json_file:
    solardata = json.load(json_file)
    day = solardata[dateStr]
    sunrise = day['sunrise']
    sunset = day['sunset']
    # print(f"Sunrise: {sunrise} - sunset: {sunset}")

sunriseHour = int(sunrise[0:2])
sunriseMinute = int(sunrise[3:5])
sunriseToday = mytz.replace(hour=sunriseHour,minute=sunriseMinute, second=0, microsecond=0)

sunsetHour = int(sunset[0:2])
sunsetMinute = int(sunset[3:5])
sunsetToday = mytz.replace(hour=sunsetHour,minute=sunsetMinute, second=0, microsecond=0)
startCountDown = sunriseToday - timedelta(hours=2)
startCountUp = sunsetToday + timedelta(hours=2)

#print("")
# print(f"startCountDown {startCountDown}")
# print(f"startCountUp {startCountUp}")
# print(f"Sunset {sunsetToday}")
#print(f"Start Countdown {startCountdown}")
# print(f"Start CountdownP {startCountdownP}")
#print(mytz > startCountdown)

# for i in range(120):
#     startCountdown = startCountdown + timedelta(minutes=1)
#     ex = int(localStorage.getItem('exposure'));    
#     print(f"{startCountdown}: {ex}")
#     ex = ex - 50390
#     localStorage.setItem('exposure', ex)

exposureRatio = 50390

def getCurrentExposure():
    returnedValue = False
    if (mytz < startCountDown or mytz > startCountUp):
        returnedValue = True
        print(exposure_max)
    elif (mytz > startCountDown and mytz < startCountUp):
        checkCountDown = localStorage.getItem('countDown')
        # print(f"checkCountDown: {checkCountDown}")
        if (checkCountDown != 'on'):
            checkCountDown = 'on'
            max_exposure = 6000000
            localStorage.setItem('countDown', checkCountDown)
            localStorage.setItem('countUp', 'off')
            currentExposure = max_exposure-exposureRatio
            localStorage.setItem('currentExposure', currentExposure)
            returnedValue = True
            print(currentExposure)
        else: 
            currentExposure = localStorage.getItem('currentExposure')
            print(f"CurrentExposure {currentExposure}")
            if (currentExposure == 'None'):
                currentExposure = 1000
                print("ERROR")
            if (int(currentExposure)<2000):
                localStorage.setItem('currentExposure', 2000)
                returnedValue = True
                print(2000)
            else:
                localStorage.setItem('currentExposure', currentExposure)
                returnedValue = True
                print(currentExposure)
    else:
        checkCountUp = localStorage.getItem('countUp')
        # print(f"checkCountUp: {checkCountUp}")
        if (checkCountUp != 'on'):
            checkCountDown = 'off'
            checkCountUp = 'on'
            max_exposure = 6000000
            localStorage.setItem('countDown', 'off')
            localStorage.setItem('countUp', checkCountUp)
            currentExposure = int(localStorage.getItem('currentExposure'))+exposureRatio
            localStorage.setItem('currentExposure', currentExposure)
            returnedValue = True
            print(currentExposure)
        else: 
            currentExposure = int(localStorage.getItem('currentExposure'))+exposureRatio
            localStorage.setItem('currentExposure', currentExposure)
            if (currentExposure>6000000):
                returnedValue = True
                print(6000000)
            else:
                returnedValue = True
                print(currentExposure)        

    if not returnedValue:
        # print("No return value")
        print(int(localStorage.getItem('currentExposure')))

getCurrentExposure()