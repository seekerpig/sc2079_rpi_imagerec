#This is for sending and receiving image from RPI
from server import *
import os 
import shutil
import time
import glob
import torch
from PIL import Image
from model import *
import subprocess
#from imutils import paths


def init():
    print("Initialising image recognition....")
    imageServer = Server()
    imageServer.start()


if __name__ == "__main__":
    init()
    run_yolov5_server()
