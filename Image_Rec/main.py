#This is for sending and receiving image from RPI
import Server

def init():
    print("Initialising image recognition....")
    imageServer = Server()
    imageServer.start()
    


if __name__ == "__main__":
    init()
