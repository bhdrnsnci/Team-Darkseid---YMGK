import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont


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

camera = cv2.VideoCapture(1)
while True:
    ret, frame = camera.read()
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

    cv2.imshow('camera', frame)
    k = cv2.waitKey(10) & 0xff
    if k == 27 or k == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
