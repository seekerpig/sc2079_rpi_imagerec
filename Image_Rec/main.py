#This is for sending and receiving image from RPI
from server import *
import os 
import shutil
import time
import glob
import torch
from PIL import Image
#from imutils import paths


def init():
    print("Initialising image recognition....")
    imageServer = Server()
    imageServer.start()

def load_model():
    model = torch.hub.load('./', 'custom', path='best.pt', source='local')
    return model

def predict_image(image_path):
    model = load_model()
    img = Image.open(image_path)
    result = model(img)
    results.save('runs')
    return result


if __name__ == "__main__":
    init()
