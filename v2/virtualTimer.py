#!/usr/bin/env /usr/local/bin/python3.9
import pytz
import json
from datetime import datetime, time, timezone, timedelta
import os
import sys
from localStoragePy import localStoragePy
from logger import silentlog

localStorage = localStoragePy('ekstremedia-timelapse-exposure', 'sqlite')
tz = pytz.timezone('Europe/Oslo')
js = os.path.join(sys.path[0], "data/solartimes.json")

# mytz = datetime.now()
def getCurrentExposure():
    max_exposure = 5000000
    exposureRatio = 30390
    min_exposure = 2000
    default_exposure = min_exposure
    # mytz = datetime(2021,2,5,15,34)
    mytz = datetime.now()
    mytz = tz.localize(mytz)
    # print(f"mytz: {mytz}")
    day = mytz.strftime('%d')                               # 05
    month = mytz.strftime('%m')
    dateStr = day+"-"+month
    hour = mytz.strftime('%H:%M')                               # 05
    # print(f"Now: {mytz}")
    # print(f"Hour {hour}")
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
    # print(f"Mytz: {mytz}")

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

    sunriseToday = mytz.replace(hour=sunriseHour,minute=sunriseMinute, second=0, microsecond=0)
    sunsetToday = mytz.replace(hour=sunsetHour,minute=sunsetMinute, second=0, microsecond=0)

    # print(f"Sunrise: {sunriseToday}")
    # print(f"Sunset: {sunsetToday}")
    # {'data': True, 'sunrise': '08:32', 'solar_noon': '12:12', 'sunset': '15:52'}
    #                                                                       17:05
    # 8:50
    # old 150
    timeToStartDay = sunriseToday - timedelta(minutes=180)
    # timeToStartDay = sunriseToday - timedelta(hours=1)

    #old = 120
    endOfDay = sunsetToday + timedelta(minutes=135)
    # print(f"Time to start day: {timeToStartDay}")
    # old = 50
    timeToEndDay = sunsetToday + timedelta(minutes=20)
    currentExposure = 5000000
    # print(currentExposure)
    # print(getExposure)
    if (mytz < timeToStartDay or mytz > endOfDay):
        currentExposure = max_exposure
    else:
        getExposure = localStorage.getItem('currentExposure')
        if (str(getExposure) == 'None'):
            if (mytz < timeToStartDay or mytz > endOfDay):
                # print(f"None set, defaulting to {max_exposure}")
                localStorage.setItem('currentExposure', max_exposure)
                currentExposure = max_exposure
            elif(mytz>= timeToStartDay and mytz <= endOfDay):
                # print(f"None set, defaulting to {default_exposure}")
                localStorage.setItem('currentExposure', default_exposure)
                currentExposure = default_exposure
        # else:

        if (str(getExposure) != 'None'):        
            currentExposure = int(getExposure)

            # print(currentExposure)
    if (mytz > timeToStartDay and mytz < timeToEndDay):
        # print(currentExposure)
        if (currentExposure > min_exposure):
            currentExposure = currentExposure-exposureRatio
            if (currentExposure < min_exposure):
                currentExposure = min_exposure
        else:
            currentExposure = min_exposure
    elif (mytz > timeToStartDay and mytz > timeToEndDay):
        if (currentExposure < max_exposure):
            currentExposure = currentExposure+exposureRatio
            if (currentExposure > max_exposure):
                currentExposure = max_exposure

    localStorage.setItem('currentExposure', currentExposure)
    silentlog(f"Exposure: {currentExposure}")
    return int(currentExposure)

# mytz = datetime(2021,2,5,7,4)
# for i in range(140):
#     mytz = mytz + timedelta(minutes=1)
#     hr = mytz.strftime('%H:%M')
#     ex = getCurrentExposure()

#     ps = f"Time: {hr}, ex: {ex}"
#     print(ps)
    

