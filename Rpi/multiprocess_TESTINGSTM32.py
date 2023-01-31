#Other essential libraries
from multiprocessing import Process, Value, Manager, Queue

#Communication classes
from Android import Android
from STM32 import STM32
from Algo import Algo
from imageClient import ImageClient

#Extra config / helpers
import Protocol
import ast



class MultiProcess:
    def __init__(self):
        print("Starting multi processing __init__ function")
        manager = Manager()
        #initialising the modes path = 1
        self.mode = 0 

        #initialising all the classes first
        self.Android = Android()
        self.STM32 = STM32()
        self.Algo = Algo()
        self.ImageRec =  ImageClient()
        
        #creating some movement and event locks
        self.movement_lock = manager.Lock()
        self.unpause = manager.Event()

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
            #self.Algo.connect()
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
                    
                    if rawMessage.startswith(Protocol.Android.TASK1):
                        #If message is for doing task 1, the message should consist of two parts, header and obstacle coordinates
                        # "TASK1|[{x:6,y:2,d:4}, {x:4,y:2,d:0}, {x:5,y:2,d:2}]" THE COORDINATE REPRESENTS OBSTACLE HERE
                        
                        messageList = rawMessage.split(Protocol.MSG_SEPARATOR)
                        if (len(messageList) > 1):
                            self.mode = 1
                            self.toAlgoQueue.put_nowait(rawMessage)
                            self.unpause.set()
                        else:
                            print("Message is from android for task 1 is not complete, hence not processed.")
                        

                    elif rawMessage.startswith(Protocol.Android.TASK2):
                        #TODO task 2 for the project
                        self.unpause.set()
                        pass

                    elif rawMessage.startswith(Protocol.Android.MANUAL):
                        #If message is for MANUAL movement, the message should consist of two parts, header and command
                        # "MANUAL|FR00"
                        messageList = rawMessage.split(Protocol.MSG_SEPARATOR)
                        if (len(messageList) > 1):
                            self.mode = 0 
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
                 #rawMessage = self.Algo.receive()

                 #type the commands algo will send here
                 #e.g.
                 rawMessage = input("Enter a message from receiving from Algo")

                 if rawMessage is None:
                     continue

                 if rawMessage.startswith(Protocol.Algo.TASK1): 
                    
                     messageList = rawMessage.split(Protocol.MSG_SEPARATOR)

                     if (len(messageList) == 3):
                        
                             #Sending the message from the list individually to the queue
                             #example, FW10 , FW00 etc... 
                             message_list = ast.literal_eval(messageList[1])
                             for item in message_list:
                                  self.toSTMQueue.put_nowait(item)

                             #Sending the Robot coordinates to Android
                             if self.mode == 1: 
                                self.toAndroidQueue.put_nowait(messageList[2])
                                self.unpause.set()

                
            except Exception as error:
                print("Receive from algo error:", error)


    def sendToAlgo(self):
        while True:
            try:
                if not self.toAlgoQueue.empty():
                    message = self.toAlgoQueue.get_nowait()
                    #self.Algo.send(message)
                    print("")
                    print("Message being sent to Algo...")
                    print("Message is: ", message)
                
            except Exception as error:
                print("Send to algo error:", error)

    
    def receiveFromSTM(self):
        while True:
            raw_massage = self.STM32.recv()
                
            if raw_massage is None:
                    continue
            try: 
                if raw_massage.startswith("ACK"): 
                    
                    # Ack sent therefore releasing lock 
                    self.movement_lock.release()
                    print("ACK received, Movement lock releasing . . .")
                    
                    #Check if its on path mode then inform android the next position
                    if self.mode==1: 
                       self.toAndroidQueue.put_nowait("NEXT") 

                if raw_massage.startswith("FAILED"):
                    self.movement_lock.release()
                    self.toAndroidQueue.put_nowait("FAILED")
                    print("Error detected , Movement lock releasing . . .")
                               
            except Exception as error:
                    print("STM Read Error:", error)

                
    def sendToSTM(self):
        while True:
            try:
                #Block execution and acquire lock
                if not self.toSTMQueue.empty():
                    message = self.toSTMQueue.get_nowait()
                    self.unpause.wait()
                    self.movement_lock.acquire()

                    # Instructions for STM if the message is part of movements
                    if any(message.startswith(v) for v in Protocol.Movements.__dict__.values()):
                        self.STM32.send(message) 

                    # Command for taking picture
                    elif message == "SNAP": 
                        self.toImageQueue.put_nowait(message)

                    # Completed the run  
                    elif message == "FIN":
                        self.unpause.clear()
                        self.movement_lock.release()
                        print("Instruction Completed!") 
                    else: 
                        raise Exception(f"Unknown instruction: {message}")

            except Exception as error:
                 print('Process sendToSTM has failed:', error)

    #you expect to get the message back from imageRec when sending, so no receive function
    def sendToImageRec(self):
        while True:
            try:
                if not self.toImageQueue.empty():
                    message = self.toImageQueue.get_nowait()
                    #self.Algo.send(message)
                    print("")
                    print("Message being sent to Image Rec...")
                    print("Message is: ", message)

                    print("Assuming image rec has performed image rec successfully..")
                    print("Image id detected is 13, sending to Android Queue recognised image id")
                    self.toAndroidQueue.put_nowait("IMAGEID|13")

                    #release lock so we can send new commands to STM32.
                    self.movement_lock.release()

                
            except Exception as error:
                print("Send to image rec error:", error)

    
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
