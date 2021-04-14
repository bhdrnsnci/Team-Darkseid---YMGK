import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from flask import Flask, Response, render_template

app = Flask(__name__)

def stream():
    def print_utf8_text(image, xy, text, color):
        fontName = 'tahoma.ttf'
        font = ImageFont.truetype(fontName, 24)
        img_pil = Image.fromarray(image)
        draw = ImageDraw.Draw(img_pil)
        draw.text((xy[0], xy[1]), text, font=font, fill=(color[0], color[1], color[2], 0))
        image = np.array(img_pil)
        return image

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    recognizer.read('training/trainer.yml')
    cascadePath = "face.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath);
    font = cv2.FONT_HERSHEY_SIMPLEX
    id = 0
    names = ['None', 'Bahadır Nişancı', 'Mustafa Kemal Atatürk', 'Neşe Hanım', 'Enver Paşa']

    camera = cv2.VideoCapture(0)
    while True:
        _, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            if (confidence < 100):
                id = names[id]
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                id = "bilinmiyor"
                confidence = "  {0}%".format(round(100 - confidence))

            color = (255, 255, 255)
            frame = print_utf8_text(frame, (x + 5, y - 25), str(id), color)
            cv2.putText(frame, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        imgShow = cv2.imencode('.jpg', frame)[1]
        imgData = imgShow.tobytes()
        yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+imgData+b'\r\n')


def stream1():
    def print_utf8_text(image, xy, text, color):
        fontName1 = 'tahoma.ttf'
        font1 = ImageFont.truetype(fontName1, 24)
        img_pil1 = Image.fromarray(image)
        draw1 = ImageDraw.Draw(img_pil1)
        draw1.text((xy[0], xy[1]), text, font=font1, fill=(color[0], color[1], color[2], 0))
        image = np.array(img_pil1)
        return image

    recognizer1 = cv2.face.LBPHFaceRecognizer_create()
    recognizer1.read('training/trainer.yml')
    cascadePath1 = "face.xml"
    faceCascade1 = cv2.CascadeClassifier(cascadePath1);
    font1 = cv2.FONT_HERSHEY_SIMPLEX
    id = 0
    names = ['None', 'Bahadır Nişancı', 'Mustafa Kemal Atatürk', 'Neşe Hanım', 'Enver Paşa']

    camera1 = cv2.VideoCapture(1)
    while True:
        _, frame1 = camera1.read()
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        faces1 = faceCascade1.detectMultiScale(gray1, scaleFactor=1.2, minNeighbors=5)
        for (x, y, w, h) in faces1:
            cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, confidence = recognizer1.predict(gray1[y:y + h, x:x + w])
            if (confidence < 100):
                id = names[id]
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                id = "bilinmiyor"
                confidence = "  {0}%".format(round(100 - confidence))

            color = (255, 255, 255)
            frame = print_utf8_text(frame1, (x + 5, y - 25), str(id), color)
            cv2.putText(frame1, str(confidence), (x + 5, y + h - 5), font1, 1, (255, 255, 0), 1)

        imgShow1 = cv2.imencode('.jpg', frame1)[1]
        imgData1 = imgShow1.tobytes()
        yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n'+imgData1+b'\r\n')



@app.route('/camera')
def camera():
    return Response(stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/camera1')
def camera1():
    return Response(stream1(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/register')
def parse1():
    import creating
    import training
    return render_template('main.html')


@app.route('/cameras')
def cameras():
    return render_template('cameras.html')


@app.route('/')
def index():
    return render_template('main.html')

@app.route('/users')
def parse2():
    return render_template('main.html')


@app.route('/guests')
def parse3():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
    app.debug = True
