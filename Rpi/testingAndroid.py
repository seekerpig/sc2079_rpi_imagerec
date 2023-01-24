#Other essential libraries
from multiprocessing import Process, Value, Manager, Queue

#Communication classes
from Android import Android






class MultiProcess:
    def __init__(self):
        print("Starting multi processing __init__ function")
        self.manager = Manager()

        #initialising all the classes first
        self.Android = Android()
        #self.STM32 = STM32()
        #self.Algo = Algo()
        #self.ImageRec =  ImageClient()
        

        #creating message queues for each of the relevant process
        self.toAndroidQueue = Queue()
        #self.toAlgoQueue = Queue()
        #self.toSTMQueue = Queue()
        #self.toImageQueue = Queue()

        #creating threads/processes for each of the classes
        #7 processes
        self.receiveFromAndroidProcess = Process(target= self.receiveFromAndroid)
        self.sendToAndroidProcess = Process(target= self.sendToAndroid)
        #self.receiveFromAlgoProcess = Process(target= self.receiveFromAlgo)
        #self.sendToAlgoProcess = Process(target= self.sendToAlgo)
        #self.receiveFromSTMProcess = Process(target= self.receiveFromSTM)
        #self.sendToSTMProcess = Process(target= self.sendToSTM)
        #self.sendToImageRecProcess = Process(target= self.sendToImageRec)

    def start(self):
        #this function would try to establish all the connections
        try:
            print("Starting connections..")
            self.Android.connect()
            #self.Algo.connect()
            #self.STM32.connect()
            #I think imageRec no need connect? not sure
            #self.ImageRec.connect()
            print("Connections successful.")


            #after connection, start all the processes to begin running
            print("Starting processes..")
            self.receiveFromAndroidProcess.start()
            self.sendToAndroidProcess.start()
            #self.receiveFromAlgoProcess.start()
            #self.sendToAlgoProcess.start()
            #self.receiveFromSTMProcess.start()
            #self.sendToSTMProcess.start()
            #self.sendToImageRecProcess.start()
            #print("Processes started.")

        except Exception as error:
            print("Error when starting multiprocess.start connections: ", error)

        
        #self.checkProcesses()
    
    def end(self):
        if self.Android is not None:
            self.Android.disconnect()
        
        #if self.Algo is not None:
            #self.Algo.disconnect()
        
        #if self.STM32 is not None:
            #self.STM32.disconnect()
        
        print("Multiprocessing has stopped.. All connections are disconnected.")

    def receiveFromAndroid(self):
        while True:
            try:
                rawMessage = self.Android.receive()
                
                if(rawMessage):
                    #TODO need to implement code to check below for who message is for and then do the message process
                    print("Checking receiveFromAndroid process work... rawMessage = ", rawMessage)

                    #testing only - add message to androidQueue to see if it sends to android a not.
                    self.toAndroidQueue.put_nowait("Hello World")
                    pass

                
            except Exception as error:
                print("Receive from android error:", error)
    
    def sendToAndroid(self):
        while True:
            try:
                if not self.toAndroidQueue.empty():
                    message = self.toAndroidQueue.get_nowait()
                    self.android.send(message)
                
            except Exception as error:
                print("Send to android error:", error)
                


    
    def checkProcesses(self):
        #this is a while loop on the main thread.
        while True:
            try:
                #Type some code below here to check whether the connections are live?
                #if not live, must reconnect?
                pass
            except Exception as error:
                print("checkProcesses error: ", error)
