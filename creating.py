import cv2

camera = cv2.VideoCapture(1)
camera.set(3, 640)
camera.set(4, 480)
face_detector = cv2.CascadeClassifier('face.xml')
face_id = input('\n Id: ')
face_name = input('\n Ad: ')
count = 0

while (True):
    ret, img = camera.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        count += 1

        cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y + h, x:x + w])
        cv2.imshow('image', img)
    k = cv2.waitKey(300) & 0xff
    if k == 27:
        break
    elif count >= 60:
        break

camera.release()
cv2.destroyAllWindows()