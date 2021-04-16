import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from flask import Flask, Response, render_template, redirect, url_for, request
import os

app = Flask(__name__)

global userData
userData = ""

#   Webcam
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
                id = "bilinmeyen kişi"
                confidence = "  {0}%".format(round(100 - confidence))

            color = (255, 255, 255)
            frame = print_utf8_text(frame, (x + 5, y - 25), str(id), color)
            cv2.putText(frame, str(confidence), (x + 5, y + h - 5), font, 1, (0, 255, 0), 1)

        imgShow = cv2.imencode('.jpg', frame)[1]
        imgData = imgShow.tobytes()
        yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n' + imgData + b'\r\n')
    #   Ipcam


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
        yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n' + imgData1 + b'\r\n')


@app.route('/camera')
def camera():
    return Response(stream(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/camera1')
def camera1():
    return Response(stream1(), mimetype='multipart/x-mixed-replace; boundary=frame')


def streamLoginCamera():
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
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX
    id = 0
    names = ['None', 'Bahadır Nişancı', 'Mustafa Kemal Atatürk', 'Neşe Hanım', 'Enver Paşa']

    camera = cv2.VideoCapture(1)
    control = 0
    verification = 0
    userData = ""
    cam = True
    while cam:
        _, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            id, confidence = recognizer.predict(gray[y:y + h, x:x + w])
            if (confidence < 100):
                id = names[id]
                confidence = "  {0}%".format(round(100 - confidence))
                if control == 5:
                    if verification >= 3:
                        print(userData)
                        cam = False
                    control = 0
                    verification = 0
                if control == 0:
                    userData = id
                if control != 5 and control != 0:
                    if userData == id:
                        verification += 1
            else:
                id = "Bilinmeyen Kişi"
                confidence = "  {0}%".format(round(100 - confidence))

            control += 1
            color = (255, 255, 255)
            frame = print_utf8_text(frame, (x + 5, y - 25), str(id), color)
            cv2.putText(frame, str(confidence), (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        imgShow = cv2.imencode('.jpg', frame)[1]
        imgData = imgShow.tobytes()
        yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n' + imgData + b'\r\n')


@app.route('/loginCamera')
def loginCamera():
    return Response(streamLoginCamera(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/cameras')
def cameras():
    return render_template('cameras.html')


def streamCreate():
    camera = cv2.VideoCapture(1)
    camera.set(3, 640)
    camera.set(4, 480)
    face_detector = cv2.CascadeClassifier('face.xml')
    face_id = input('\n Id: ')
    face_name = input('\n Ad: ')
    count = 0
    cam = True
    while cam:
        _, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            count += 1
            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])

        imgShow = cv2.imencode('.jpg', frame)[1]
        imgData = imgShow.tobytes()
        yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n' + imgData + b'\r\n')

        k = cv2.waitKey(300) & 0xff
        if k == 27:
            cam = False
        elif count >= 60:
            cam = False



def training():
    path = 'dataset'
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("face.xml")

    def getImagesAndLabels(path):
        imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
        faceSamples = []
        ids = []
        for imagePath in imagePaths:
            PIL_img = Image.open(imagePath).convert('L')
            img_numpy = np.array(PIL_img, 'uint8')
            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = detector.detectMultiScale(img_numpy)
            for (x, y, w, h) in faces:
                faceSamples.append(img_numpy[y:y + h, x:x + w])
                ids.append(id)
        return faceSamples, ids

    print("\n Bu işlem biraz uzun sürebilir. Lütfen bekleyin...")
    faces, ids = getImagesAndLabels(path)
    recognizer.train(faces, np.array(ids))
    recognizer.write('training/trainer.yml')
    print("\n Tamamlandı.".format(len(np.unique(ids))))

    #   Yüz kayıt


@app.route('/createCam')
def createCam():
    return Response(streamCreate(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/create')
def create():
    return render_template('create.html')


@app.route('/redirec')
def redirec():
    return render_template('redirect.html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/loginFunc')
def loginFunc():
    print("asdf")
    return render_template("login.html")


@app.route('/register')
def register():
    return render_template('register.html')


@app.route('/users')
def parse2():
    return render_template('main.html')


@app.route('/guests')
def parse3():
    return render_template('index.html')


if __name__ == '__main__':
    app.run()
