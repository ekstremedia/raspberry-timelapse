import subprocess as sp

temp  = sp.getoutput('/opt/vc/bin/vcgencmd measure_temp')
print(temp)