# A test of OpenCV's frontal face detection capabilities.
# from: http://docs.opencv.org/trunk/doc/py_tutorials/py_objdetect/py_face_detection/py_face_detection.html

import numpy as np
import cv2

# TODO: get XML from portable directory-- this is the Haar cascades XML
# config file, usually found in OpenCV's data directory
face_cascade = cv2.CascadeClassifier('/usr/local/share/OpenCV/haarcascades/haarcascade_frontalface_default.xml')

img = cv2.imread('f4.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

faces = face_cascade.detectMultiScale(gray, 1.3, 5)
face_count = 1
for (x,y,w,h) in faces:
    roi_gray = gray[y:y+h, x:x+w]
    roi_color = img[y:y+h, x:x+w]
    cv2.imwrite('testout' + str(face_count) + '.jpg', img[y:y+h, x:x+w])
    face_count += 1

cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows()
