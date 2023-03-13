#Other essential libraries
from multiprocessing import Process, Value, Manager, Queue

#Communication classes
from Android import Android
from STM32 import STM32
from Algo import Algo
from imagecapturefinal import ImageClient
import time

#Extra config / helpers
import Protocol
import ast



class MultiProcess:
    def __init__(self):
        print("Starting multi processing __init__ function")
        manager = Manager()
        #initialising the modes path = 1
        self.mode = 0 
        self.count = 1
        self.task2Count = Value('i', 0)
        self.task2Distance = Value('i', 0)
        #initialising all the classes first
        self.Android = Android()
        self.STM32 = STM32()
        #self.Algo = Algo()
        #self.ImageRec =  ImageClient()
        
        #creating some movement and event locks
        self.movement_lock = manager.Lock()
        self.unpause = manager.Event()

        #creating message queues for each of the relevant process
        self.toAndroidQueue = Queue()
        #self.toAlgoQueue = Queue()
        self.toSTMQueue = Queue()
        self.toImageQueue = Queue()

        #creating threads/processes for each of the classes
        #7 processes
        self.receiveFromAndroidProcess = Process(target= self.receiveFromAndroid)
        self.sendToAndroidProcess = Process(target= self.sendToAndroid)
        #self.receiveFromAlgoProcess = Process(target= self.receiveFromAlgo)
        #self.sendToAlgoProcess = Process(target= self.sendToAlgo)
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
            #self.receiveFromAlgoProcess.start()
            #self.sendToAlgoProcess.start()
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
                #self.toAndroidQueue.put_nowait("Hello Android")

                if(rawMessage):
                    #TODO need to implement code to check below for who message is for and then do the message process
                    print("Checking receiveFromAndroid process work... rawMessage = ", rawMessage)
                    
                    if rawMessage.startswith(Protocol.Android.TASK1):
                        #If message is for doing task 1, the message should consist of two parts, header and obstacle coordinates
                        # "TASK1|[{'x':6,'y':2,'d':4,'id':1}, {'x':4,'y':2,'d':0, 'id':2 }, {'x':5,'y':2,'d':2, 'id':3}]"  THE COORDINATE REPRESENTS OBSTACLE HERE
                        
                        messageList = rawMessage.split(Protocol.MSG_SEPARATOR)
                        if (len(messageList) > 1):
                            self.mode = 1
                            self.toAlgoQueue.put_nowait(rawMessage)
                            self.unpause.set()
                            
                        else:
                            print("Message from android for task 1 is not complete, hence not processed. Length of message lesser than 2.")
                        

                    elif rawMessage.startswith(Protocol.Android.TASK2):
                        #TODO task 2 for the project
                        hardcoded_path = [
                        "FW01", "SNAP1" #next command is FL00 or FR00 but its appended by the image rec, so its not in this hardcoded string
                        ]
                        for c in hardcoded_path:
                            self.toSTMQueue.put_nowait(c)
                        self.unpause.set()

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
                    elif (rawMessage.startswith("A5TASK")):
                        self.unpause.set()
                        self.navigateSingleObstacle()
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

                    #type the commands algo will send here
                    #e.g. "TASK1|['FW10','FIN']|[{'x':1,'y':1,'d':0, 's':0}, {'x':4,'y':2,'d':2. 's':0}]"
                    #e.g. "TASK1|['FR00','FIN']|[{'x':1,'y':1,'d':0, 's':0}, {'x':4,'y':2,'d':2. 's':0}]"
                    #e.g. "TASK1|['BR00']|[{'x':1,'y':1,'d':0, 's':0}]"
                    #e.g. "TASK1|['FR00','FW30','FIN']|[{'x':1,'y':1,'d':0, 's':0}]"
                    #rawMessage = "TASK1|['BR00','FIN']|[{'x':9,'y':2,'d':0, 's':0}]"
                    #rawMessage = None
                    # if rawMessage is None:
                    #     continue

                    if rawMessage.startswith(Protocol.Algo.TASK1): 
                        print("mesage from algo is: ", rawMessage)
                        messageList = rawMessage.split(Protocol.MSG_SEPARATOR)

                        if (len(messageList) == 3):
                        
                            #Sending the message from the list individually to the queue
                            #example, FW10 , FW00 etc... 
                            message_list = ast.literal_eval(messageList[1])
                            for item in message_list:
                                self.toSTMQueue.put_nowait(item)

                            #Sending the Robot coordinates to Android
                            #if self.mode == 1: 
                            self.toAndroidQueue.put_nowait("PATHS|" + messageList[2])
                            print("message okay 123")
                            self.unpause.set()

                
            except Exception as error:
                print("Receive from algo error:", error)


    def sendToAlgo(self):
        while True:
            try:
                if not self.toAlgoQueue.empty():
                    message = self.toAlgoQueue.get_nowait()
                    self.Algo.send(message)
                    print("")
                    print("Message being sent to Algo...")
                    print("Message is: ", message)

                    #for testing purposes only.
                    #self.receiveFromAlgo()
                
            except Exception as error:
                print("Send to algo error:", error)

    
    def receiveFromSTM(self):
        while True:
            raw_message = self.STM32.recv()
            
            if raw_message is None:
                    continue
            try: 
                print("Message received from STM:", raw_message)
                if raw_message.startswith("A"): 
                    
                    # Ack sent therefore releasing lock 
                    # print(self.mode)
                    # if self.mode==1: 
                    #self.toAndroidQueue.put_nowait("NEXT")

                    print("ACK received, Movement lock releasing . . .")
                    self.movement_lock.release()
                    
                    #Check if its on path mode then inform android the next position
                    # if self.mode==1: 
                    #    self.toAndroidQueue.put_nowait("NEXT") 
                elif raw_message.startswith("D"):
                    #get the distance after D and store it.
                    #HOPEFULLY THIS ONE NO storing issue
                    self.task2Distance = int(raw_message[1:])
                    print("distance stored is, ",self.task2Distance)
                    print("D received, Movement lock releasing . . .")
                    self.movement_lock.release()

                # Take_Picture|left. to determine which lane is the robot at
                elif raw_message.startswith("Take_Picture"):
                    self.movement_lock.release()
                    message = raw_message.split(Protocol.MSG_SEPARATOR)
                    if (len(message) > 1):
                        if (raw_message[1] == "left"):
                            self.toSTMQueue.put_nowait("FL")

                        elif (raw_message[1] == "right"):
                            self.toSTMQueue.put_nowait("FR")
                    else:
                        self.toImageQueue.put_nowait("Take_Picture")
                        print("Proceeding to take picture, Movement lock releasing . . . .")

                elif raw_message.startswith("Swerve_completed"):
                    self.movement_lock.release()
                    self.toSTMQueue.put_nowait("Forward_to_obs")
                    print("Proceeding to move forward, Movement lock releasing . . . .")
                               
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

                    print("message sent to stm", message)
                    
                    if any(message.startswith(v) for v in Protocol.Movements.__dict__.values()):
                        #time.sleep(0.2)
                        self.STM32.send(message) 
                   
                    # Completed the run  
                    #elif message == "FIN":
                       # self.unpause.clear()
                       # self.movement_lock.release()
                       # print("Instruction Completed!") 
                    else: 
                        raise Exception(f"Unknown instruction: {message}")

            except Exception as error:
                 print('Process sendToSTM has failed:', error)

    #you expect to get the message back from imageRec when sending, so no receive function
    def sendToImageRec(self):
        camera = ImageClient()
        while True:
            try:
                if not self.toImageQueue.empty():
                    message = self.toImageQueue.get_nowait()
                    #self.Algo.send(message)
                    print("")
                    print("Message being sent to Image Rec...")
                    #print("Message is: ", message)
                    #count = message[-1]
                    result = None
                    result = camera.snap_and_detect()
                    #result['image_id'] = 38
                    print("Result from image rec to rpi is: ", result)
                    
                    
                    #self.toAndroidQueue.put_nowait("IMAGEID|COUNT|RESULT")
                    #self.toAndroidQueue.put_nowait("IMAGEID|"+str(result['image_id']))
                    #self.toAndroidQueue.put_nowait("NEXT")
                    #self.count +=1
                    #self.movement_lock.release()
                    if result != None:
                        #print("Testing")
                        #print(result['image_id'])
                        if(result['image_id'] == 38):
                            #print("38")
                            #right arrow
                            if(self.task2Count == 0):
                                print("FR00")
                                #THIS RUNS AFTER THE FIRST SNAP DONE BY IMAGE REC
                                #SO WE send 3 command, if the image is right arrow for first obstacle
                                #FR00 to serve around the robot from the right then to the middle
                                #FW02 for second ultrasonic run
                                #SNAP2 for taking picture of second obstacle
                                self.toSTMQueue.put_nowait("FR00") 
                                self.toSTMQueue.put_nowait("FW02")
                                self.toSTMQueue.put_nowait("SNAP2")
                                self.task2Count = 1
                            elif(self.task2Count == 1):
                                print("BR00")
                                #THIS RUNS AFTER THE SECOND SNAP DONE BY IMAGE REC
                                #SO if second image is RIGHT arrow, we send BR00 for big right turn
                                #then we send FL10 for a left turn to curve into the back of the obstacle after the big right turn
                                #then FW50 for travelling the distance of the big obstacle? this one might not be 50, can be 40 or 60, test it on the day
                                #then FL20 which stands for the a different left turn that will make the robot finish the turn about of the obstacle
                                #afterwards travel FWXX distance based on the XX distance send to us by STM32
                                #afterwards we use FL30 serve into the same column as carpark after crossing the first obstacle u
                                #afterwards we FW03 to finish the ultrasonic into the carpark and auto stop.
                                self.toSTMQueue.put_nowait("BR00")
                                self.toSTMQueue.put_nowait("FL10")
                                self.toSTMQueue.put_nowait("FW50")
                                self.toSTMQueue.put_nowait("FL20")
                                someString = "FW" + str(self.task2Distance)
                                self.toSTMQueue.put_nowait(someString)
                                self.toSTMQueue.put_nowait("FL30")
                                self.toSTMQueue.put_nowait("FW03")
                                
                                self.toSTMQueue.put_nowait("BR00")
                        elif(result['image_id'] == 39):
                            #print("39")
                            #left arrow
                            if(self.task2Count == 0):
                                print("FL00")
                                #THIS RUNS AFTER THE FIRST SNAP DONE BY IMAGE REC
                                #SO WE send 3 command, if the image is LEFT arrow for first obstacle
                                #FL00 to serve around the robot from the left then to the middle
                                #FW02 for second ultrasonic run
                                #SNAP2 for taking picture of second obstacle
                                self.toSTMQueue.put_nowait("FL00")
                                self.toSTMQueue.put_nowait("FW02")
                                self.toSTMQueue.put_nowait("SNAP2")
                                self.task2Count = 1
                            elif(self.task2Count == 1):
                                print("BL00")
                                #THIS RUNS AFTER THE SECOND SNAP DONE BY IMAGE REC
                                #SO if second image is LEFT arrow, we send BR00 for big LEFT turn
                                #then we send FR10 for a right turn turn to curve into the back of the obstacle after the big left turn
                                #then FW50 for travelling the distance of the big obstacle? this one might not be 50, can be 40 or 60, test it on the day
                                #then FR20 which stands for the a different RIGHT turn that will make the robot finish the turn about around the obstacle
                                #afterwards travel FWXX distance based on the XX distance send to us by STM32
                                #afterwards we use FR30 serve into the same column as carpark after crossing the first obstacle.
                                #afterwards we FW03 to finish the ultrasonic into the carpark and auto stop.
                                self.toSTMQueue.put_nowait("BL00")
                                self.toSTMQueue.put_nowait("FR10")
                                self.toSTMQueue.put_nowait("FW50")
                                self.toSTMQueue.put_nowait("FR20")
                                someString = "FW" + str(self.task2Distance)
                                self.toSTMQueue.put_nowait(someString)
                                self.toSTMQueue.put_nowait("FL30")
                                self.toSTMQueue.put_nowait("FW03")
                                
                        else:
                            print("do nothing image id not 38 or 39")
    

                    #release lock so we can send new commands to STM32.
                    # if(result != None):
                    #     if result['image_id'] == 41 :
                    #         self.movement_lock.release()
                    #         turn = "FR00", "FL00", "FW30", "BR00", "FW10", "SNAP"
                    #         for i in turn :
                    #             self.toSTMQueue.put_nowait(i)
                    #     else:
                    #         self.movement_lock.release()
                    #         self.toSTMQueue.put_nowait("FIN")
                    #dont need this for now, this is for actual task.
                    #self.toAndroidQueue.put_nowait("IMAGEID|1|13")

                    #basically if an image is detected and the symbol is 41, then we dont do anything
                    #if symbol is not 41, then we know non bulleyes, means we can clear the command queue to stop 
                    #sending more commands to move

                    #ONLY UNCOMMENT THIS PART FOR CLEARING TASK A5 I think.
                    # if(result['image_id'] != 'NA'):
                    #     # stop issuing commands
                    #     self.unpause.clear()

                    #     # clear commands queue
                    #     while not self.command_queue.empty():
                    #         self.command_queue.get()

                    #     print("Found non-bullseye face, remaining commands and path cleared.")
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


    def navigateSingleObstacle(self):
        # travel around obstacle until image detected (non bulleye)

        
        # hardcoded_path = [
        #     "SNAP",
        #     "FR00", "FL00", "FW30", "BR00", "FW10", "SNAP",
        #     "FR00", "FL00", "FW30", "BR00", "FW10", "SNAP",
        #     "FR00", "FL00", "FW30", "BR00", "FW10", "SNAP",
        #     "FR00", "FL00", "FW30", "BR00", "FW10", "SNAP",
        #     "FIN"
        # ]
        hardcoded_path = ["SNAP"]   
        # hardcoded_path = [
        #     "DT20", "SNAP", "NOOP",
        #     "FR00", "FL00", "FW30", "BR00", "FW10", "SNAP", "NOOP",
        #     "FR00", "FL00", "FW30", "BR00", "FW10", "SNAP", "NOOP",
        #     "FR00", "FL00", "FW30", "BR00", "FW10", "SNAP", "NOOP",
        #     "FIN"
        # ]

        # put commands and paths into queues
        self.clear_queues()
    
        for c in hardcoded_path:
            self.toSTMQueue.put_nowait(c)
            #dont need to tell android i believe, so never talk to android.
            # self.path_queue.put({
            #     "d": 0,
            #     "s": -1,
            #     "x": 1,
            #     "y": 1
            # })

        print("Navigate-around-obstacle path loaded. Robot is ready to move.")    
