import imagezmq
import cv2
#pip install imagezmq
#pip install opencv-python

class Server:
    def __init__(self):
        self.image_receiver = imagezmq.ImageHub()

    def start(self):
        try:
            #image_receiver.bind_to('tcp://*:6666')

            while True:
                print("Waiting for image to be received....")
                sender, img = self.image_receiver.recv_image()
                print(f'Received image from {sender}')

                cv2.imshow(sender, img)
                cv2.waitKey(0); cv2.destroyAllWindows(); cv2.waitKey(1)
                self.image_receiver.send_reply(b'OK')
        
        except Exception as e:
            print("Error occured: " + str(e))