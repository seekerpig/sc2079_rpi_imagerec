#actual code
#from multiprocess import MultiProcess


#testing android code
from testingAndroid import MultiProcess

def init():
    print("Starting up group 6 rpi")
    #add code below to call a multi processing class to create
    #the different processes and start them all up
    multiprocessor = MultiProcess
    multiprocessor.start()


    #testing the imagezmq library
    #imageClient = ImageClient()
    #imageClient.takePhoto()
    #imageClient.stop()


if __name__ == "__main__":
    init()
