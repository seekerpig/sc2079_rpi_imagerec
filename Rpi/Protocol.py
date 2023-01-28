class header:
  STM = 'STM,'.encode()
  Android = 'AND,'.encode()
  COMMA_SEPARATOR = ",".encode()
 

# Movements
class Movements:

  FW = 'FW'.encode()
  FL = 'FL'.encode()
  FR = 'FR'.encode()
  BW = 'BW'.encode()
  BL = 'BL'.encode()
  BR = 'BR'.encode()

#STM messages
class STM_status:
  COMPLETED = 'COMPLETED,'.encode()
  REACH = 'REACH,'.encode()

#Android to Algo
#OBSTACLE message = "ALG,OBSTACLE,
class AndtoAlgo:
  OBSTACLE = "OBSTACLE".encode()
  START = 'START,'.encode()
  
#Android to STM
#MANUAL MESSAGE should look like this: STM,MANUAL,FW10
 
class AndToSTM:
  MANUAL = 'MANUAL,'.encode()

#Android to RPI
class AndTORPI:
  SNAP = 'SNAP,'.encode()
  STOP = 'STOP,'.encode()
  START = 'START,'.encode()

#Algo to STM
#MOVEMENTS MESSAGE should look like this: "STM,MOVEMENTS,["FW10","FR00","FW50","SNAP","FIN"]"
class AlgoToSTM:
  path ='path,'.encode() #??

#Algo to Android
class AlgoToAnd: 
    ROBOT  = "ROBOT,".encode() #??
