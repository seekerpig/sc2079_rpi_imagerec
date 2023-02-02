import cv2
import imutils
import numpy as np
import pytesseract
import socket
from PIL import Image
from picamera.array import PiRGBArray
from picamera import PiCamera
import pprint

camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))
count = 0
IP = "192.168.24.242"
PORT = 5005
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((IP, PORT))

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        image = frame.array
        cv2.imshow("Frame", image)
        key = cv2.waitKey(1) & 0xFF
        rawCapture.truncate(0)
    
        if key == ord("s"):
            camera.capture("Images/"+str(count)+".jpg")
            TEST_IMAGE = "Images/"+str(count)+".jpg"
            image_data = open(TEST_IMAGE, "rb").read()
            s.sendall(image_data)
            response = s.recv(1024)
            pprint.pprint(response)
            count+=1
        if key == ord("a"):
            cv2.destroyAllWindows()
            break
cv2.destroyAllWindows()
s.close()
