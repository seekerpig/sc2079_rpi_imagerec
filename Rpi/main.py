

#testing STM32
from multiprocess_TESTINGSTM32 import MultiProcess

#testing android code
#from testingAndroid import MultiProcess

def init():
    try:
        print("Starting up group 6 rpi")
        #add code below to call a multi processing class to create
        #the different processes and start them all up
        multiprocessor = MultiProcess()
        multiprocessor.start()


        #testing the imagezmq library
        #imageClient = ImageClient()
        #imageClient.takePhoto()
        #imageClient.stop()
    except KeyboardInterrupt:
        print("Keyboard interrupted, ending multiprocess")
        multiprocessor.end()
    
    except Exception as error:
        print("Error has occured: ", error)
        multiprocessor.end()


if __name__ == "__main__":
    init()
