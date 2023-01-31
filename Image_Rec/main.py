#This is for sending and receiving image from RPI
from server import *
import os 
import shutil
import time
import glob
import torch
from PIL import Image
from model import *
#from imutils import paths


def init():
    print("Initialising image recognition....")
    imageServer = Server()
    imageServer.start()

def image_predict():
    # save the image file to the uploads folder
    file = request.files['file']
    filename = file.filename
    print(filename)
    file.save(os.path.join('uploads', filename))

if __name__ == "__main__":
    init()
