ffmpeg \
  -i /var/www/html/videoer/nodeflicker.mp4 \
  -i /var/www/html/videoer/deflicker.mp4 \
  -filter_complex '[0:v]pad=iw*2:ih[int];[int][1:v]overlay=W/2:0[vid]' \
  -map [vid] \
  -c:v libx264 \
  -crf 23 \
  -preset veryfast \
  /var/www/html/videoer/combined.mp4
