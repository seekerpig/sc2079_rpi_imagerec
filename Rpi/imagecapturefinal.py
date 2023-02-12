import cv2
import imutils
import numpy as np
import pytesseract
from PIL import Image
from picamera.array import PiRGBArray
from picamera import PiCamera
import pprint
import requests

class ImageClient:
    def __init__(self):
        self.camera = PiCamera()
        self.camera.resolution = (640, 480)
        self.camera.framerate = 30
        self.rawCapture = PiRGBArray(self.camera, size=(640, 480))
        self.count = 0
        self.DETECTION_URL = "http://192.168.24.242:5005/Test"

    def capture_and_detect(self):
        for frame in self.camera.capture_continuous(self.rawCapture, format="bgr", use_video_port=True):
            image = frame.array
            cv2.imshow("Frame", image)
            key = cv2.waitKey(1) & 0xFF
            self.rawCapture.truncate(0)
        
            if key == ord("s"):
                self.camera.capture("Images/"+str(self.count)+".jpg")
                TEST_IMAGE = "Images/"+str(self.count)+".jpg"
                image_data = open(TEST_IMAGE, "rb").read()
                response = requests.post(self.DETECTION_URL, files={"image": image_data}).json()
                pprint.pprint(response)
                self.count+=1
            if key == ord("a"):
                cv2.destroyAllWindows()
                break
        cv2.destroyAllWindows()
        
    def snap_and_detect(self):
                self.camera.capture("Images/"+str(self.count)+".jpg")
                TEST_IMAGE = "Images/"+str(self.count)+".jpg"
                image_data = open(TEST_IMAGE, "rb").read()
                response = requests.post(self.DETECTION_URL, files={"image": image_data}).json()
                pprint.pprint(response)
                self.count+=1 
                return response   

def main():
    image_capture = ImageClient()
    image_capture.capture_and_detect()

if __name__ == "__main__":
    main()
