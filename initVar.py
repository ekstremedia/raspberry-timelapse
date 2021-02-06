#!/usr/bin/env /usr/local/bin/python3.9
from localStoragePy import localStoragePy
from virtualTimer import getCurrentExposure
localStorage = localStoragePy('ekstremedia-timelapse-exposure', 'sqlite')

#localStorage.setItem('countDown', 'on')
#localStorage.setItem('countUp', 'off')

# print(f"countUp: {localStorage.getItem('countUp')}")
# print(f"countDown: {localStorage.getItem('countDown')}")
# print(f"currentExp: {localStorage.getItem('currentExposure')}")

ex = getCurrentExposure()
print(ex)