import socket
import sys
import io

from ultralytics import YOLO
from PIL import Image
# create a socket object
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# get local machine name
host = '127.0.0.1'
port = 10050

# bind to the port
serversocket.bind((host, port))

# queue up to 5 requests
serversocket.listen(5)
model = YOLO('MDP.pt')
while True:
    # establish a connection
    clientsocket, addr = serversocket.accept()

    print("Got a connection from %s" % str(addr))

    # receive the size of the image data
    size_data = clientsocket.recv(1024)
    size = int.from_bytes(size_data,byteorder='big')

    # receive the actual image data
    data = b''
    received_size = 0
    while received_size < size:
        part = clientsocket.recv(1024)
        data += part
        received_size += len(part)
    #img = Image.open(io.BytesIO(data))
    # validate that all of the data has been received
    if len(data) != size:
        print("Error: Incomplete data received")
    else:
        with open("received_image.jpg", "wb") as f:
            f.write(data)
        f.close()
        results = model.predict("received_image.jpg",show = True,save=True,save_txt=True,save_conf = True,save_crop=True)
        

        results = bytes(str(results), 'utf8')

        clientsocket.send(results)

    clientsocket.close()
