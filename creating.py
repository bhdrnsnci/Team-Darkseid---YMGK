import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from flask import Flask, Response, render_template, redirect, url_for, request, session
import sqlite3
import os


def streamCreate():
    print("1")
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
        print("w")
        _, frame = camera.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x, y, w, h) in faces:
            print("f")
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
            count += 1
            cv2.imwrite("dataset/"+ face_ad +"." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])

        imgShow = cv2.imencode('.jpg', frame)[1]
        imgData = imgShow.tobytes()
        yield (b'--frame\r\n'b'Content-Type: text/plain\r\n\r\n' + imgData + b'\r\n')

        k = cv2.waitKey(300) & 0xff
        if k == 27:
            cam = False
        elif count >= 5:
            cam = False

streamCreate()