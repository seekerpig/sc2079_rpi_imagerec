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
class AndtoAlgo:
  OBSTACLE = "OBSTACLE".encode()
  START = 'START,'.encode()
  
#Android to STM
class AndToSTM:
  MANUAL = 'MANUAL,'.encode()

#Android to RPI
class AndTORPI:
  SNAP = 'SNAP,'.encode()
  STOP = 'STOP,'.encode()
  START = 'START,'.encode()

#Algo to STM
class AlgoToSTM:
  path ='path,'.encode() #??

#Algo to Android
class AlgoToAnd: 
    ROBOT  = "ROBOT,".encode() #??