import cv2
import os

class VideoCamera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)
        self.img_counter = 0

    def __del__(self):
        self.video.release()        

    def get_frame(self):
        ret, frame = self.video.read()

        # DO WHAT YOU WANT WITH TENSORFLOW / KERAS AND OPENCV

        ret, jpeg = cv2.imencode('.jpg', frame)

        return jpeg.tobytes()
    
    def save_frame(self):
        ret, frame = self.video.read()

        img_name = "opencv_frame_{}.png".format(self.img_counter)
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        self.img_counter += 1