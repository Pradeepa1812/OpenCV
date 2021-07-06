from flask import Flask,render_template,Response
import cv2

app=Flask(__name__)
camera=cv2.VideoCapture(0)


@app.route('/')
def index():
    return render_template('index.html')




def generate_frames():
    while True:
        #Read the camera frame
        success,frame=camera.read()
        if not success:
            break
        else:
            face_cascade=cv2.CascadeClassifier('C:/Users/Pradeepa/.spyder-py3/haarcascade_frontface.xml')
            eye_cascade=cv2.CascadeClassifier('C:/Users/Pradeepa/.spyder-py3/haarcascade_eye.xml')
            
            face=face_cascade.detectMultiScale(frame,1.1,7)
            gray=cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
            
            #draw rectangle around each face
            for (x,y,w,h) in face:
                cv2.rectangle(frame,(x,y),(x+w,y+h),(255,128,21),3)
                roi_gray=gray[y:y+h,x:x+w]
                roi_color=frame[y:y+h,x:x+w]
                
                eyes=eye_cascade.detectMultiScale(roi_gray,1.1,7)
                for (ex,ey,ew,eh) in eyes:
                    cv2.rectangle(roi_color,(ex,ey),(ex+ew,ey+eh),(12,32,45),3)
                    
            
            
            
            #encodes an image into a memory buffer
            ret,buffer= cv2.imencode('.jpg',frame)  #encode the entire code in the form of jpg or png
            frame= buffer.tobytes() #convert buffer back to bytes
        #if your images is in the byte type we need to pass Content-Type
        yield(b'--frame\r\n'
              b'Content-Type:image/jpeg\r\n\r\n'+frame+b'\r\n')



@app.route('/video')
def video():
    return Response(generate_frames() ,mimetype='multipart/x-mixed-replace;boundary=frame')

if __name__=='__main__':
    app.run(debug=True)