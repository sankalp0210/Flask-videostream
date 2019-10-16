#!/usr/bin/env python
from importlib import import_module
import os
from flask import Flask, render_template, Response, url_for, redirect
from camera_opencv import Camera
import subprocess
from time import sleep
global_frame = open('img.jpg', 'rb').read()

app = Flask(__name__)
tm = 5
is_video = True
@app.route('/')
def index():
    """Video streaming home page."""
    global is_video
    is_video = True
    return render_template('index.html')

@app.route('/video')
def video():
    """Video streaming home page."""
    if is_video:
        return render_template('video.html', is_video = True)
    else:
        return render_template('video.html', is_video = False)

@app.route('/result')
def result():
    bashCommand = "python3 file.py"
    output = subprocess.check_output(['bash','-c', bashCommand])
    sleep(5)
    bashCommand = "sshpass -p \"Fingerface!\" scp -r output user@ada.iiit.ac.in:~"
    output = subprocess.check_output(['bash','-c', bashCommand])
    bashCommand = "sshpass -p \"Fingerface!\" ssh output user@ada.iiit.ac.in \"bash test.sh\""
    output = subprocess.check_output(['bash','-c', bashCommand])
    sleep(30)
    bashCommand = "sshpass -p \"Fingerface!\" scp -r user@ada.iiit.ac.in:~/out.txt ."
    output = subprocess.check_output(['bash','-c', bashCommand])
    bashCommand = "cat out.txt"
    output = subprocess.check_output(['bash','-c', bashCommand])
    return render_template('result.html')

def gen(camera):
    """Video streaming generator function."""
    val = 1
    global is_video
    while True:
        frame = camera.get_frame()
        if frame != None:
            val = 0
            yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
        elif val:
            continue
        else:
            is_video = False
            break
    yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + global_frame + b'\r\n')

@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='127.0.0.1', threaded=True)
