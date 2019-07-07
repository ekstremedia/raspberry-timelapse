#!/bin/bash
echo "Starting timelapse"
raspistill -awb cloud -o still%05d.jpg -tl 10000 -t 86400000 -ex verylong
