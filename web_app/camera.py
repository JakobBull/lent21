import cv2
import os
import sys

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.img_counter = 0

    def __del__(self):
        self.video.release()        

    def get_frame(self):
        ret, frame = self.video.read()

        ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes()

    def save_frame(self):
        ret, frame = self.video.read()
        path = os.getcwd() + '/static/'
        print(path + "opencv_frame_{}.png".format(self.img_counter))
        img_name = path + "opencv_frame_{}.png".format(self.img_counter)
        print(img_name)
        written = cv2.imwrite(img_name, frame)
        if written == 1:
            print("{} written!".format(img_name))
        self.img_counter += 1

        return "opencv_frame_{}.png".format(self.img_counter-1)