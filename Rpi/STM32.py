import time
import serial
from misc.protocols import STM_PROTOCOL
from misc.config import SERIAL_PORT, BAUD_RATE

class STM:
    def __init__(self, serial_port=SERIAL_PORT, baud_rate=BAUD_RATE) -> None:
        self.baud_rate = baud_rate
        self.serial_port = serial_port
        self.stm = none 
    #Establish connection with STM Board
    def connect(self) -> None:
        retry = True
        while retry:
            try:
                print(f"[STM] Establishing Connection with STM on Serial Port: {self.serial_port} Baud Rate: {self.baud_rate}")
                self.stm = serial.Serial(port=self.serial_port, baudrate=self.baud_rate, timeout=None)
                if self.stm is not None:
                    print(f"[STM] Established connection on Serial Port: {self.serial_port} Baud Rate: {self.baud_rate}")
                    retry = False
            except IOError as error:
                print(f"[Error] Failed to establish STM Connection, retrying connection!")
                retry = True
    
    def disconnect(self) -> None:
        print(f"[STM] Disconnecting STM ...")
        try:
                self.stm.close()
                self.stm = None
                print(f"[STM] STM has been disconnected.")
        except Exception as error:
            print(f"[Error] Failed to disconnect STM")

    def recv(self, timeout:float =0.5, retries:int = 5 ) -> str:
    for i in range(retries):
        try:
            self.stm.timeout = timeout 
            if self.stm.inWaiting() > 0:
                    message = self.stm.read(self.stm.inWaiting()).strip().decode("utf-8")
                    return message
            return None
        except serial.SerialTimeoutException as error:
                print(f"[Error] Failed to recieve from STM: {str(error)}. Retrying...")
                time.sleep(timeout)
        raise Exception("Failed to receive data from STM after multiple retries")
        
    def send(self, message) -> None:
        try:
            print(f"[STM] Message to STM: {message}")
            self.stm.write(message.encode("utf-8")))
        except Exception as error:
            print(f"[Error] Failed to send to STM: {str(error)}")



