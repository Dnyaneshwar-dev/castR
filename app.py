from flask import Flask, render_template, Response
import cv2
import socket
app = Flask(__name__)

hostname = socket.gethostname()
ip_address = socket.gethostbyname(hostname)

camera = cv2.VideoCapture(0) 

def gen_frames():  
    while True:
        success, frame = camera.read() 
       
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/')
def starter():
    return render_template('starter.html',title='started',ip = ip_address,port=8080)


if __name__ == '__main__':
    app.run(host=ip_address,port=8080)