import bluetooth
import os

#configurations for bluetooth
UUID = ""
BLUETOOTH_ADDR = ""

class Android:
    def __init__(self):
        print("Android init")

        #make bluetooth discoverable on rpi
        os.system("sudo hciconfig hci0 piscan")

        #declare connections
        self.server_sock= bluetooth.BluetoothSocket(bluetooth.RFCOMM)
        self.server_sock.bind(("",bluetooth.PORT_ANY))
        self.server_sock.listen(1)
        
        self.port = self.server_sock.getsockname()[1]

        bluetooth.advertise_service(self.server_sock, "MDP_Group_06",
                   service_id = bluetooth.SERIAL_PORT_CLASS,
                   service_classes = [bluetooth.SERIAL_PORT_CLASS ],
                   profiles = [bluetooth.SERIAL_PORT_PROFILE ])

        

    def connect(self):
        #perform connection
        print(f"Connecting Android.. waiting for bluetooth connection on RFCOMM {self.port}..")
        retry = True
        self.client_sock = None
        while retry:
            try:
                if self.client_sock == None:
                    self.client_sock,self.address = self.server_sock.accept()
                    print("Accepted connection from ",self.address)
                    retry = False

            except Exception as error:
                print("Failed to connect to establish bluetooth connection with Android, retrying...")
                retry = True

                if(self.client_sock != None):
                    print("Client socket not none, closing socket for retry")
                    self.client_sock.close()
                    self.client_sock = None

        #self.client_sock.send("testing this message".encode("utf-8"))
    
    def disconnect(self):
        #disconnect
        print("Disconnecting Android..")
        try:
            self.client_sock.close()
            #self.server_sock.close()
            #self.server_sock = None
            self.client_sock = None

        except Exception as error:
            print("Failed to disconnect android client socket...")

    
    def send(self, message):
        #sending message
        print("")
        print("Sending message to Android, message: ", message)
        try:
            self.client_sock.send(message.encode("utf-8"))
        
        except Exception as error:
            print("Error sending message to android: ". error)

    def receive(self):
        #receiving message
        print("")
        print("receiving message from Android")
        self.data = self.client_sock.recv(1024).decode("utf-8")
        self.data = self.data.strip()
        #print("received data from android:", self.data)

        return self.data