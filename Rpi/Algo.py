#socket for communication
import socket


IP_ADDR = "192.168.6.6"
PORT = "5050"


class Algo:
    def __init__(self):
        #declare connections
        print("Algo init")

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #SO_REUSEADDR, is a socket option that allows a socket to bind to a port that is already in use by another socket.
        #This option is typically used when a server is being restarted and it needs to bind to the same port that it was using before.
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket.bind((IP_ADDR, PORT))
        self.server_socket.listen(5)

    def connect(self):
        #perform connection
        print(f"Connecting Algo.. waiting for socket connection on IP_ADDR {IP_ADDR} and PORT {PORT}..")
        retry = True
        self.client_sock = None
        while retry:
            try:
                if self.client_sock == None:
                    self.client_sock,self.address = self.server_socket.accept()
                    print("Accepted algo connection from ",self.address)
                    retry = False

            except Exception as error:
                print("Failed to connect to establish connection with algo, retrying...")
                retry = True

                if(self.client_sock != None):
                    print("Client socket not none, closing socket for retry")
                    self.client_sock.close()
                    self.client_sock = None

        #self.client_sock.send("testing this algo message".encode("utf-8")) 
    
    def disconnect(self):
        #disconnect
        print("Disconnecting algo..")
        try:
            self.client_socket.close()
            #self.server_socket.close()
            #self.server_socket = None
            self.client_sock = None

        except Exception as error:
            print("Failed to disconnect algo client socket...")
    
    def send(self, message):
        #sending message
        print("")
        print("Sending message to Algo, message: ", message )
        try:
            self.client_sock.send(message.encode("utf-8"))
        
        except Exception as error:
            print("Error sending message to algo: ". error)

    def receive(self):
        #receiving message
        print("")
        print("receiving message from Algo")
        self.data = self.client_sock.recv(1024).decode("utf-8")
        self.data = self.data.strip()
        #print("received data from algo: ", self.data)

        return self.data

# some testing code
if __name__ == "__main__":
    server = Algo()
    server.connect()

    while True:
        msg = input("Type a message to send to client algo")
        server.send(msg)

        receivedMsg = server.receive()
        if (receivedMsg):
            print(f"Received message from algo client: {receivedMsg}")