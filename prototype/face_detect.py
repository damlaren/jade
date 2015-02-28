# A test of OpenCV's frontal face detection capabilities.
# from: http://docs.opencv.org/trunk/doc/py_tutorials/py_objdetect/py_face_detection/py_face_detection.html

import numpy as np
import cv2
import glob
import os
import sys

# Read script arguments.
if len(sys.argv) < 3:
    print "usage: python face_detect.py <data-dir> <output-dir> [xml-dir]\n" \
          "\tdata-dir: directory containing input data (profile photos)\n" \
          "\toutput-dir: directory in which to dump output images\n" \
          "\txml-dir: directory containing XML configuration file\n"
    sys.exit(1)

data_dir = sys.argv[1]
output_dir = sys.argv[2]
xml_dir = '/usr/local/share/OpenCV/haarcascades'
if len(sys.argv) > 3:
    xml_dir = sys.argv[3]
print "data directory is: " + data_dir
print "output directory is: " + output_dir
print "xml directory is: " + xml_dir

# Create detector.
face_cascade = cv2.CascadeClassifier(xml_dir + "/haarcascade_frontalface_default.xml")

# Iterate through all pictures and apply the detection algorithm.
i = 0
for file_path in glob.glob(data_dir + "/*.jpg"):
    img = cv2.imread(file_path)
    file_name = os.path.basename(file_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    face_index = 1
    for (x,y,w,h) in faces:
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        output_file_name = "%s/out_%02d_%s" %(output_dir, face_index, file_name)
        cv2.imwrite(output_file_name, img[y:y+h, x:x+w])
        face_index += 1
    i += 1
    if i % 1000 == 0:
    	print "Finished: ", i

#cv2.imshow('img',img)
#cv2.waitKey(0)
#cv2.destroyAllWindows()
