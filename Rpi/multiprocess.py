#Other essential libraries
import cv2
import imagezmq
from multiprocessing import Process, Value, Manager, Queue

#Communication classes
from Android import Android
from STM32 import STM32
from Algo import Algo
from imageClient import ImageClient

#Image Rec Classes
from picamera import PiCamera
from imageClient import *





class MultiProcess:
    def __init__(self):
        print("Starting multi processing __init__ function")
        self.manager = Manager()

        #initialising all the classes first
        self.Android = Android()
        self.STM32 = STM32()
        self.Algo = Algo()
        self.ImageRec =  ImageClient()
        

        #creating message queues for each of the relevant process
        