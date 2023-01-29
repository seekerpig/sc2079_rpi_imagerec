#This is for sending and receiving image from RPI
from server import *
import os 
import shutil
import time
import glob
import torch
from PIL import Image
from imutils import paths

def load_model():
    model = torch.hub.load('./', 'custom', path='./model.pt', source='local')
    return model

def init():
    print("Initialising image recognition....")
    imageServer = Server()
    imageServer.start()
    


if __name__ == "__main__":
    init()
