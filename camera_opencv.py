import os
import cv2
from base_camera import BaseCamera
from time import time

class Camera(BaseCamera):
    video_source = 0

    def __init__(self):
        if os.environ.get('OPENCV_CAMERA_SOURCE'):
            Camera.set_video_source(int(os.environ['OPENCV_CAMERA_SOURCE']))
        super(Camera, self).__init__()

    @staticmethod
    def set_video_source(source):
        Camera.video_source = source

    @staticmethod
    def frames():
        camera = cv2.VideoCapture(Camera.video_source)
        if not camera.isOpened():
            raise RuntimeError('Could not start camera.')

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        out = cv2.VideoWriter('output.avi',fourcc, 20.0, (640,480))
        out2 = cv2.VideoWriter('frames.avi',fourcc, 20.0, (640,480))
        cnt = 0
        # tm = time()
        # while camera.isOpened() and (time() - tm) < 5:
        while camera.isOpened():
            cnt += 1
            ret, img = camera.read()
            if ret==True:
                out.write(img)
                if cnt >= 10 and cnt%5 == 0:
                    out2.write(img)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
            else:
                break
            yield cv2.imencode('.jpg', img)[1].tobytes()

        camera.release()
        out.release()
        out2.release()
