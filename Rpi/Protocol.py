




MSG_SEPARATOR = "|"


#HERE ARE MESSAGES FROM ANDROID:
class Android:
  #Examples of possible messages for manual:
  # "MANUAL|FW10" 
  # "MANUAL|FR00"
  MANUAL = "MANUAL"
  #Examples of possible messages for TASK1:
  # "TASK1|[{'x':6,'y':2,'d':4}, {'x':4,'y':2,'d':0}, {'x':5,'y':2,'d':2}]" THE COORDINATE REPRESENTS OBSTACLE HERE
  TASK1 = "TASK1"
  TASK2 = "TASK2" 

#HERE ARE MESSAGES FROM ALGO:
class Algo:
  # "TASK1|['FW10', 'FR00', 'FW70', 'BR00', 'BW20', 'SNAP', 'FW20', 'FIN']|[{'x':1,'y':1,'d':0, 's':0}, {'x':4,'y':2,'d':2. 's':0}, {'x':5,'y':2,'d':2, 's':1}]" THE COORDINATE REPRESENTS WHERE THE ROBOT WILL BE AT (NOT OBSTACLE)
  TASK1 = "TASK1"
  TASK2 = "TASK2"

class STM:
  ACK = "ACK"
  


 

# Movements
class Movements:
  FW = 'FW'
  FL = 'FL'
  FR = 'FR'
  BW = 'BW'
  BL = 'BL'
  BR = 'BR'



SYMBOL_MAP = {
    "NA": "NA",
    "11": "One",
    "12": "Two",
    "13": "Three",
    "14": "Four",
    "15": "Five",
    "16": "Six",
    "17": "Seven",
    "18": "Eight",
    "19": "Nine",
    "20": "A",
    "21": "B",
    "22": "C",
    "23": "D",
    "24": "E",
    "25": "F",
    "26": "G",
    "27": "H",
    "28": "S",
    "29": "T",
    "30": "U",
    "31": "V",
    "32": "W",
    "33": "X",
    "34": "Y",
    "35": "Z",
    "36": "Up Arrow",
    "37": "Down Arrow",
    "38": "Right Arrow",
    "39": "Left Arrow",
    "40": "Stop",
    "41": "Bullseye"
}






# #STM messages
# class STM_status:
#   COMPLETED = 'COMPLETED,'.encode()
#   REACH = 'REACH,'.encode()

# #Android to Algo
# #OBSTACLE message = "ALG,OBSTACLE,
# class AndtoAlgo:
#   OBSTACLE = "OBSTACLE".encode()
#   START = 'START,'.encode()
  
# #Android to STM
# #MANUAL MESSAGE should look like this: STM,MANUAL,FW10
 
# class AndToSTM:
#   MANUAL = 'MANUAL,'.encode()

# #Android to RPI
# class AndTORPI:
#   SNAP = 'SNAP,'.encode()
#   STOP = 'STOP,'.encode()
#   START = 'START,'.encode()

# #Algo to STM
# #MOVEMENTS MESSAGE should look like this: "STM,MOVEMENTS,["FW10","FR00","FW50","SNAP","FIN"]"
# class AlgoToSTM:
#   path ='path,'.encode() #??

# #Algo to Android
# class AlgoToAnd: 
#     ROBOT  = "ROBOT,".encode() #??
