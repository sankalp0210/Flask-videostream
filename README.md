flask-video-streaming
=====================

Command to check no. of frames -
ffmpeg -i frames.avi -vcodec copy -f rawvideo -y /dev/null 2>&1 | tr ^M '\n' | awk '/^frame=/ {print $2}'|tail -n 1

