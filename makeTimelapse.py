#!/usr/bin/env python3.9
import sys
import os
import subprocess as sp

target_folder = sys.argv[1]
output_filename = sys.argv[2]
extension = '*.jpg'
print(f"Looking for: {target_folder+extension}")
print(f"Outputting to: {output_filename}")
over = f"find {target_folder+extension} -type f -size -100k | wc -l"
overdelete = f"find {target_folder+extension} -type f -size -100k -delete"
overexposed = sp.getoutput(over)
if int(overexposed)>0:
    print(f"Deleting {overexposed} overexposed images...")
    delete = sp.getoutput(overdelete)
else:
    print("No overexposed images found")

ffmpeg_cmd = f"ffmpeg -r 25 -pattern_type glob -i '{target_folder+extension}' -c:v libx264 {output_filename}"
print(ffmpeg_cmd)
# sp.call(ffmpeg_cmd)
#sp.call(['ffmpeg', '-r', '25', '-pattern glob' '-i', ])
sp.call(ffmpeg_cmd, shell="True")