#!/usr/bin/env /usr/local/bin/python3.9
from localStoragePy import localStoragePy

localStorage = localStoragePy('ekstremedia-timelapse-exposure', 'sqlite')

localStorage.setItem('countDown', 'on')
localStorage.setItem('countUp', 'off')