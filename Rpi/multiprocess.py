#Other essential libraries
from multiprocessing import Process, Value, Manager, Queue

#Communication classes
from Android import Android
from STM32 import STM32
from Algo import Algo
from imageClient import ImageClient





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
        self.toAndroidQueue = Queue()
        self.toAlgoQueue = Queue()
        self.toSTMQueue = Queue()
        self.toImageQueue = Queue()

        #creating threads/processes for each of the classes
        #7 processes
        self.receiveFromAndroidProcess = Process(target= self.receiveFromAndroid)
        self.sendToAndroidProcess = Process(target= self.sendToAndroid)
        self.receiveFromAlgoProcess = Process(target= self.receiveFromAlgo)
        self.sendToAlgoProcess = Process(target= self.sendToAlgo)
        self.receiveFromSTMProcess = Process(target= self.receiveFromSTM)
        self.sendToSTMProcess = Process(target= self.sendToSTM)
        self.sendToImageRecProcess = Process(target= self.sendToImageRec)

    def start(self):
        #this function would try to establish all the connections
        try:
            self.Android.connect()
            self.Algo.connect()
            self.STM32.connect()

            #I think imageRec no need connect? not sure
            #self.ImageRec.connect()
        except Exception as error:
            print("Error when starting multiprocess.start connections: ", error)
    
    def receiveFromAndroid(self):
        while True:
            try:
                #
                pass
            except Exception as error:
                print(error)
                raise error
    
    def sendToAndroid(self):
        while True:
            try:
                pass
            except Exception as error:
                print(error)
                raise error

    

    def receiveFromAlgo(self):
        while True:
            try:
                pass
            except Exception as error:
                print(error)
                raise error


    def sendToAlgo(self):
        while True:
            try:
                pass
            except Exception as error:
                print(error)
                raise error

    
    def receiveFromSTM(self):
        while True:
            try:
                pass
            except Exception as error:
                print(error)
                raise error
    def sendToSTM(self):
        while True:
            try:
                pass
            except Exception as error:
                print(error)
                raise error
    

    #you expect to get the message back from imageRec when sending, so no receive function
    def sendToImageRec(self):
        while True:
            try:
                pass
            except Exception as error:
                print(error)
                raise error
