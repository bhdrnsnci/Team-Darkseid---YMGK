import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from flask import Flask, Response, render_template, redirect, url_for, request, session
import sqlite3
import os

app = Flask(__name__)
hata = ""
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
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX
    id = 1
    names = ['None']

    with sqlite3.connect("FaceDatabase.db") as facedb:
        cursor = facedb.cursor()
        cursor.execute("select * from face")
        rows = cursor.fetchall()
        for r in rows:
            names.append(r[1])

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
    faceCascade1 = cv2.CascadeClassifier(cascadePath1)
    font1 = cv2.FONT_HERSHEY_SIMPLEX
    id = 1
    names = ['None']

    with sqlite3.connect("FaceDatabase.db") as facedb:
        cursor = facedb.cursor()
        cursor.execute("select * from face")
        rows = cursor.fetchall()
        for r in rows:
            names.append(r[1])

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
                id = "Bilinmeyen Kişi"
                confidence = "  {0}%".format(round(100 - confidence))

            color = (255, 255, 255)
            frame1 = print_utf8_text(frame1, (x + 5, y - 25), str(id), color)
            cv2.putText(frame1, str(confidence), (x + 5, y + h - 5), font1, 1, (255, 255, 0), 1)

        imgShow1 = cv2.imencode('.jpg', frame1)[1]
        imgData1 = imgShow1.tobytes()
        yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n' + imgData1 + b'\r\n')

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
    id = 1
    global userData
    names = ['None']

    with sqlite3.connect("FaceDatabase.db") as facedb:
        cursor = facedb.cursor()
        cursor.execute("select * from face")
        rows = cursor.fetchall()
        for r in rows:
            names.append(r[1])

    camera = cv2.VideoCapture(0)
    control = 0
    verification = 0
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


def streamCreate():
    camera = cv2.VideoCapture(0)
    camera.set(3, 640)
    camera.set(4, 480)
    face_detector = cv2.CascadeClassifier('face.xml')

    staffdb = sqlite3.connect("FaceDatabase.db")
    cursor = staffdb.cursor()
    cursor.execute("select * from face where id = (select max(id) from staff)")
    rows = cursor.fetchall()
    face_id = rows[0][0]
    face_ad = rows[0][1]
    count = 0
    images = []
    cam = True
    while cam:
        _, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            count += 1
            cv2.imwrite("dataset/"+ face_ad +"." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])

        imgShow = cv2.imencode('.jpg', frame)[1]
        imgData = imgShow.tobytes()
        yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n' + imgData + b'\r\n')

        k = cv2.waitKey(300) & 0xff
        next = cv2.imread("image.jpg")
        nexts = cv2.imencode(".jpg", next)[1]
        nextsh = nexts.tobytes()
        if k == 27:
            cam = False
            yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n' + nextsh + b'\r\n')
        elif count >= 50:
            cam = False
            yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n' + nextsh + b'\r\n')
    training()

@app.route("/training")
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

@app.route('/loginCamera')
def loginCamera():
    return Response(streamLoginCamera(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/logout")
def logout():
    if session["logedin"] == True:
        session["logedin"] = False
        return redirect(url_for("index"))
    else:
        return redirect(url_for("login"))

@app.route("/staff", methods=["POST", "GET"])
def staff():
    if session["logedin"] == True:
        with sqlite3.connect("FaceDatabase.db") as usersdb:
            usersdb.row_factory = sqlite3.Row
            cursor = usersdb.cursor()
            cursor.execute("select * from staff")
            rows = cursor.fetchall()
            return render_template("staff.html", rows=rows)
    else:
        return redirect(url_for("login"))

@app.route("/guests", methods=["POST", "GET"])
def guests():
    if session["logedin"] == True:
        with sqlite3.connect("FaceDatabase.db") as usersdb:
            usersdb.row_factory = sqlite3.Row

            cursor = usersdb.cursor()
            cursor.execute("select * from guests")
            rows = cursor.fetchall()
            return render_template("guests.html", rows=rows)
    else:
        return redirect(url_for("login"))

@app.route('/createCam')
def createCam():
    return Response(streamCreate(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route("/registerAdmin")
def registerAdmin():
    if session["logedin"] == True:
        with sqlite3.connect("FaceDatabase.db") as vt:
            cursor = vt.cursor()
            cursor.execute("select * from admin where username = '" + session["username"] + "'")
            rows = cursor.fetchall()
            for r in rows:
                if session["username"] == r[2]:
                    return render_template("register-admin.html")
        return redirect(url_for("login"))
    else:
        return redirect(url_for("login"))

@app.route('/registerGuest')
def registerGuest():
    if session["logedin"] == True:
        with sqlite3.connect("FaceDatabase.db") as usersdb:
            cursor = usersdb.cursor()
            cursor.execute("select * from departments")
            deps = cursor.fetchall()
            return render_template('register-guest.html', deps=deps)
    else:
        return redirect(url_for("login"))

@app.route('/camera')
def camera():
    return Response(stream(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/camera1')
def camera1():
    return Response(stream1(), mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/cameras')
def cameras():
    if session["logedin"] == True:
        return render_template('cameras.html')
    else:
        return redirect(url_for("login"))

@app.route("/menu")
def menu():
    if session["logedin"] == True:
        with sqlite3.connect("FaceDatabase.db") as vt:
            cursor = vt.cursor()
            cursor.execute("select * from admin where username = '" + session["username"] + "'")
            rows = cursor.fetchall()
            for r in rows:
                if session["username"] == r[2]:
                    return render_template("menu.html")
        return render_template("menu.html", show="none")

    else:
        return redirect(url_for("login"))

@app.route("/formRegisterAdmin", methods=["POST", "GET"])
def formRegisterAdmin():
    try:
        if request.method == "POST":
            name = request.form.get("name")
            username = request.form.get("username")
            password = request.form.get("password")
            if name == "" or username == "" or password == "":
                return render_template("register-admin.html", hata="* Lütfen tüm alanları doldurun!", id="error")
            else:
                with sqlite3.connect("FaceDatabase.db") as vt:
                    cursor = vt.cursor()
                    cursor.execute("select * from admin where username = '" + username + "'")
                    rows = cursor.fetchall()
                    for r in rows:
                        if username == r[2]:
                            return render_template("register-admin.html", hata="* Kullanıcı adı zaten kayıtlı.", id="error")
                    cursor.execute("insert into admin(name, username, password) values(?, ?, ?)", (name, username, password))
                    vt.commit()
                return redirect("menu")
    except:
        return render_template("register-admin.html")


@app.route("/formLogin", methods=["POST", "GET"])
def formLogin():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        usersdb = sqlite3.connect("FaceDatabase.db")
        cursor = usersdb.cursor()
        cursor.execute("select * from staff where username = '" + username + "'")
        rows = cursor.fetchall()
        cursor.execute("select * from admin where username = '" + username + "'")
        rowsA = cursor.fetchall()
        if username == "" or password == "":
            return render_template("login.html", hata="* Lütfen tüm alanları doldurun!", id="error")

        for row in rowsA:
            if username == row[2]:
                if password == row[3]:
                    session["logedin"] = True
                    session["username"] = username
                    return redirect(url_for("menu"))
                else:
                    return render_template("login.html", hata="* Şifre yanlış!", id="error")

        for row in rows:
            if username == row[2]:
                if userData == row[1]:
                    if password == row[3]:
                        session["logedin"] = True
                        session["username"] = username
                        return redirect(url_for("menu"))
                    else:
                        return render_template("login.html", hata="* Şifre yanlış!", id="error")
                else:
                    return render_template("login.html", hata="* Sizi tanıyamadık!", id="error")
    return render_template("login.html", hata="* Kullanıcı adı yanlış!", id="error")

@app.route('/login', methods=["POST", "GET"])
def login():
    if session["logedin"] == False:
        return render_template('login.html', hata="* Lütfen kameraya bakın ve gülümseyin :)", id="complete")
    else:
        return redirect(url_for('menu'))

@app.route("/formRegisterGuest", methods=["POST", "GET"])
def formRegisterGuest():
    try:
        if request.method == "POST":
            tc = request.form.get("tc")
            name = request.form.get("name")
            address = request.form.get("address")
            phone = request.form.get("phone")
            department = request.form.get("department")
            staff = session["username"]
            if tc == "" or name == "" or address == "" or phone == "" or department == "":
                return render_template("register-guest.html", hata="* Lütfen tüm alanları doldurun!", id="error")
            else:
                with sqlite3.connect("FaceDatabase.db") as usersdb:
                    cursor = usersdb.cursor()
                    cursor.execute("select * from guests where tc = '" + tc + "'")
                    rows = cursor.fetchall()
                    for r in rows:
                        if tc == r[1]:
                            return render_template("register-guest.html", hata="* Ziyaretçi zaten kayıtlı!", id="error")

                    cursor.execute("insert into guests(tc, name, address, phone, department, staff) values(?, ?, ?, ?, ?, ?)", (tc, name, address, phone, department, staff))
                    cursor.execute("insert into face(name) values(?)", (name,))
                    usersdb.commit()
                return render_template("create.html", hata="* Bu işlem biraz uzun sürebilir lütfen bekleyin...", id="complete")
    except:
        with sqlite3.connect("FaceDatabase.db") as usersdb:
            cursor = usersdb.cursor()
            cursor.execute("select * from departments")
            deps = cursor.fetchall()
            return render_template("register-guest.html", deps=deps, hata="* Bir şeyler yolunda gitmedi :(", id="error")

@app.route("/formRegister", methods=["POST", "GET"])
def formRegister():
    try:
        if request.method == "POST":
            name = request.form.get("name")
            username = request.form.get("username")
            email = request.form.get("email")
            phone = request.form.get("phone")
            department = request.form.get("department")
            password = request.form.get("password")
            if name == "" or username == "" or email == "" or phone == "" or department == "" or password == "":
                return render_template("register.html", hata="* Lütfen tüm alanları doldurun!", id="error")
            else:
                with sqlite3.connect("FaceDatabase.db") as usersdb:
                    cursor = usersdb.cursor()
                    cursor.execute("select * from staff where username = '" + username + "' or email = '" + email + "'")
                    rows = cursor.fetchall()
                    for row in rows:
                        if username == row[2]:
                            return render_template("register.html", hata="* Kullanıcı adı zaten kayıtlı!", id="error")
                        elif email == row[3]:
                            return render_template("register.html", hata="* E Posta zaten kayıtlı!", id="error")

                with sqlite3.connect("FaceDatabase.db") as staffdb:
                    cursor = staffdb.cursor()
                    cursor.execute("insert into staff("
                                   "name, username, password, email, phone, department)"
                                   "values(?, ?, ?, ?, ?, ?)", (name, username, password, email, phone, department))
                    cursor.execute("insert into face(name) values(?)", (name,))
                    staffdb.commit()
                return render_template("create.html", hata="* Bu işlem biraz uzun sürebilir lütfen bekleyin...", id="complete")
    except:
        return render_template("register.html", hata="* Bir şeyler yolunda gitmedi :(", id="error")

@app.route('/register')
def register():
    if session["logedin"] == False:
        with sqlite3.connect("FaceDatabase.db") as usersdb:
            cursor = usersdb.cursor()
            cursor.execute("select * from departments")
            deps = cursor.fetchall()
            return render_template('register.html', deps=deps)
    else:
        return redirect(url_for("menu"))

@app.route('/')
def index():
    session["logedin"] = False
    return render_template('index.html')

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.config['SESSION_TYPE'] = 'filesystem'
    app.run(debug=True)
