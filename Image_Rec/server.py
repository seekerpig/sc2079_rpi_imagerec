import imagezmq
import cv2

class Server:
    def __init__(self):
        self.image_receiver = imagezmq.ImageHub()

    def start(self):
        try:
            #image_receiver.bind_to('tcp://*:6666')

            while True:
                print("Waiting for image to be received....")
                sender, img = image_receiver.recv_image()
                print(f'Received image from {sender}')
                cv2.imshow(sender, img)
                cv2.waitKey(1)

        
        except Exception as e:
            print("Error occured: " + str(e))
