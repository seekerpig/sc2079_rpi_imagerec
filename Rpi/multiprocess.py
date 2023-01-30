#Other essential libraries
from multiprocessing import Process, Value, Manager, Queue

#Communication classes
from Android import Android
from STM32 import STM32
from Algo import Algo
from imageClient import ImageClient
import Protocol




class MultiProcess:
    def __init__(self):
        print("Starting multi processing __init__ function")
        self.manager = Manager()

        #initialising all the classes first
        self.Android = Android()
        self.STM32 = STM32()
        self.Algo = Algo()
        self.ImageRec =  ImageClient()
        
        #creating some movement and event locks
        self.movement_lock = Manager.Lock()
        self.unpause = Manager.Event()

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
            print("Starting connections..")
            self.Android.connect()
            self.Algo.connect()
            self.STM32.connect()
            #I think imageRec no need connect? not sure
            #self.ImageRec.connect()
            print("Connections successful.")


            #after connection, start all the processes to begin running
            print("Starting processes..")
            self.receiveFromAndroidProcess.start()
            self.sendToAndroidProcess.start()
            self.receiveFromAlgoProcess.start()
            self.sendToAlgoProcess.start()
            self.receiveFromSTMProcess.start()
            self.sendToSTMProcess.start()
            self.sendToImageRecProcess.start()
            print("Processes started.")

        except Exception as error:
            print("Error when starting multiprocess.start connections: ", error)

        
        self.checkProcesses()
    
    def end(self):
        if self.Android is not None:
            self.Android.disconnect()
        
        if self.Algo is not None:
            self.Algo.disconnect()
        
        if self.STM32 is not None:
            self.STM32.disconnect()
        
        print("Multiprocessing has stopped.. All connections are disconnected.")

    def receiveFromAndroid(self):
        while True:
            try:
                rawMessage = self.Android.receive()
                
                if(rawMessage):
                    #TODO need to implement code to check below for who message is for and then do the message process
                    print("Checking receiveFromAndroid process work... rawMessage = ", rawMessage)
                    
                    if rawMessage.startwith(Protocol.Android.TASK1):
                        #If message is for doing task 1, the message should consist of two parts, header and obstacle coordinates
                        # "TASK1|[{x:6,y:2,d:4}, {x:4,y:2,d:0}, {x:5,y:2,d:2}]" THE COORDINATE REPRESENTS OBSTACLE HERE

                        messageList = rawMessage.split(Protocol.MSG_SEPARATOR)
                        if (len(messageList) > 1):
                            self.toAlgoQueue.put_nowait(rawMessage)
                            self.unpause.set()
                        else:
                            print("Message is from android for task 1 is not complete, hence not processed.")
                        

                    elif rawMessage.startwith(Protocol.Android.TASK2):
                        #TODO task 2 for the project
                        self.unpause.set()
                        pass

                    elif rawMessage.startwith(Protocol.Android.MANUAL):
                        #If message is for MANUAL movement, the message should consist of two parts, header and command
                        # "MANUAL|FR00"

                        messageList = rawMessage.split(Protocol.MSG_SEPARATOR)
                        if (len(messageList) > 1):
                            self.toSTMQueue.put_nowait(messageList[1])
                            self.unpause.set()
                        else:
                            print("Message is from android for MANUAL is not complete, hence not processed.")

                    else:
                        print("Raw message is not recognised from Android")

                    #testing only - add message to androidQueue to see if it sends to android a not.
                    #self.toAndroidQueue.put_nowait("Hello World")
                    

                
            except Exception as error:
                print("Receive from android error:", error)
    
    def sendToAndroid(self):
        while True:
            try:
                if not self.toAndroidQueue.empty():
                    message = self.toAndroidQueue.get_nowait()
                    self.Android.send(message)
                
            except Exception as error:
                print("Send to android error:", error)
                

    

    def receiveFromAlgo(self):
        while True:
            try:
                rawMessage = self.Algo.receive()
                
                if(rawMessage):
                    #TODO need to implement code to check below for who message is for and then do the message process
                    print("Checking receiveFromAlgo process work... rawMessage = ", rawMessage)

                    #testing only - add message to androidQueue to see if it sends to android a not.
                    #self.toAndroidQueue.put_nowait("Hello World")
                    pass

                
            except Exception as error:
                print("Receive from algo error:", error)


    def sendToAlgo(self):
        while True:
            try:
                if not self.toAlgoQueue.empty():
                    message = self.toAlgoQueue.get_nowait()
                    self.Algo.send(message)
                
            except Exception as error:
                print("Send to algo error:", error)

    
    def receiveFromSTM(self):
        while True:
            try:
                raw_massage = self.STM32.recv()
                
                if raw_message is None:
                    continue
                #Completed or REACH,FW,FW,Fl,FR,BW
                message = raw_messag.split(COMMA_SEPARATOR)
                
                if message[0] == STM_status.COMPLETED: # task completed
                    
                        print("Message received from STM!",message)
                        
                elif message[0] == STM_status.REACH:   # Reach location, ask RPI to take snap picture 
                    
                        print("Message received from STM!",message)
                        
                        self.toImageQueue.put_nowait(SNAP + raw_message )
                else:
                        print("Message does not match!")

            except Exception as error:
                    print("STM Read Error:", error)

                
    def sendToSTM(self):
        while True:
            try:
                #NEED TO ADD MOVEMENT LOCKS AND UNPAUSE CHECKS
                if not self.toSTMQueue.empty():
                    message = self.toSTMQueue.get_nowait()
                    self.STM32.send(message)
                
            except Exception as error:
                 print('Process sendToSTM has failed:', error)

    #you expect to get the message back from imageRec when sending, so no receive function
    def sendToImageRec(self):
        while True:
            try:
                pass
            except Exception as error:
                print(error)
                raise error

    
    def checkProcesses(self):
        #this is a while loop on the main thread.
        while True:
            try:
                #Type some code below here to check whether the connections are live?
                #if not live, must reconnect?
                pass
            except Exception as error:
                print("checkProcesses error: ", error)

    def clear_queues(self):
        while not self.toAndroidQueue.empty():
            self.toAndroidQueue.get()
        while not self.toAlgoQueue.empty():
            self.toAlgoQueue.get()
        while not self.toSTMQueue.empty():
            self.toSTMQueue.get()
        while not self.toAndroidQueue.empty():
            self.toImageQueue.get()

    @staticmethod
    def outdoorsify(original):
        # replace any turns calibrated indoor to outdoor calibrated turns.
        # replace any FW and BW to FS and BS, this is to indicate the outdoor calibrated forward and backward movements.
        if original in ["FL00", "FR00", "BL00", "BR00"]:
            return original[:2] + "20"
        elif original.startswith("FW"):
            return original.replace("FW", "FS")
        elif original.startswith("BW"):
            return original.replace("BW", "BS")
        else:
            return original