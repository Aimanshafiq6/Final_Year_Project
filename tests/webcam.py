import cv2
import sys

url = "http://192.168.0.102:8080" # Your url might be different, check the app
try:
    vs = cv2.VideoCapture(url+"/video")
except cv2.error as cv_err:
    print("[!!ERROR!!] : "+cv_err)

if not vs.isOpened():
    print("Something went wrong!!")
    sys.exit(1)

print(vs)
while True:
    ret, frame = vs.read()
    frame = cv2.resize(frame,(640,480))
    if not ret:
        continue
    # Processing of image and other stuff here
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break