from imageClient import *

def init():
    print("Starting up group 6 rpi")
    #add code below to call a multi processing class to create
    #the different processes and start them all up
    imageClient = ImageClient()
    imageClient.takePhoto()
    imageClient.stop()

    #testing the imagezmq library


if __name__ == "__main__":
    init()
