#!/usr/bin/env /usr/local/bin/python3.9

import subprocess as sp
import sys
import os
homedir = sys.path[0]
scr = os.path.join(homedir, 'getCurrentExposure.py');
exTime = sp.getoutput(scr)

print(f"Exposure time: {exTime}")
