import socket
import time
import imagezmq
import cv2
import io
import numpy as np
from picamera import PiCamera

#this one is video, not needed
#from imutils.video import VideoStream

class ImageClient:
    def __init__(self):
        self.sender = imagezmq.ImageSender(connect_to='tcp://192.168.1.98:5555')
        self.camera = PiCamera()

    def takePhoto(self):

        #this method is slow because you have to write to file system then read again
        #self.camera.capture('image.jpg')
        #self.img = cv2.imread('image.jpg')

        #optimised way to capture and read image:
        #convert the image taken to numpy array instead of saving to a file
        self.stream = io.BytesIO()
        self.camera.capture(self.stream, format='jpeg')
        self.camera.capture('Image_Rec/uploads/image.jpg')
        self.stream.seek(0)
        self.img = cv2.imdecode(np.frombuffer(self.stream.getvalue(), dtype=np.uint8), 1)


        self.reply = self.sender.send_image('RPI',self.img)
        print("Reply from receiver is: " + str(self.reply))


    
    def stop(self):
        self.sender.close()
        self.camera.close()
        