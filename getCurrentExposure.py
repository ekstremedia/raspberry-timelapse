#!/usr/bin/env /usr/local/bin/python3.9
from logger import *
import datetime
import pytz
import pandas as pd
import os
import sys
col_list = ["time", "exposure"]
usecols = col_list
homedir = sys.path[0]
csv_file = os.path.join(homedir, 'scripts/','mins.csv');
mins = pd.read_csv(csv_file, usecols=col_list)
#dateNow = str(datetime.datetime(2021,4,4,20,21,00).replace(second=0, microsecond=0))
#dateNow = datetime.datetime(2021,2,4,8,50,00).replace(second=0, microsecond=0)
dateNow = datetime.datetime.now()
tz = pytz.timezone('Europe/Oslo')
mytz = tz.localize(dateNow)
current = str(mytz.replace(second=0, microsecond=0))[0:19]
# print(current)

out = int(mins.loc[mins["time"] == current, "exposure"])
#log(f"Got shutter speed: {out}")
print(out)
