from flask import Flask, render_template, Response, jsonify, request
from camera import VideoCamera
import cv2

app = Flask(__name__)

video_stream = VideoCamera()

@app.route('/', methods=["GET", "POST"])
def index():

    if request.method == 'post':
        print('capture')
           # camera.save_frame()

    return render_template('webcam.html')

def gen(camera):
    while True:
        k = cv2.waitKey(1)
        frame = camera.get_frame()
        
        if k%256 == 32:
            print('capture')
           # camera.save_frame()

        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

def capture(camera):
    #k = cv2.waitKey(1)
    print('capture')

    #if k%256 == 32:
    camera.save_frame()

def hello():
    print('capture')

@app.route('/scan',  methods=["GET", "POST"])
def scan():
    if request.method == 'POST':
        video_stream.save_frame()
    
    return render_template('scan.html')

def gen(camera):
    while True:
        k = cv2.waitKey(1)
        #print(k)
        frame = camera.get_frame()
        
        if k%256 == 32:
            print('capture')
           # camera.save_frame()

        yield (b'--frame\r\n'
            b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')



@app.route('/video_feed', methods=["GET", "POST"])
def video_feed():
    return Response(gen(video_stream),
                mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/background_process_test')
def background_process_test(camera):
    print ("Hello")
    frame = camera.save_frame()
    return ("nothing")

if __name__ == '__main__':
    app.run(host='127.0.0.1', debug=True,port="5000")