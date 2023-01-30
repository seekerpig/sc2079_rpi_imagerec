# sc2079_rpi_imagerec
Github repository for SC2079 RPI and Image Rec - Group 06

##TODOS:
- We need to figure out what kind of messages each team will send to each other
- We need to define how those messages should look like. 
- Figure out camera height versus obstacle height, then start taking photos
- We need a function to clear queues
- What about outdoorsify?

##TODOS for 28/1/2023
What do we need to test for STM?
- Movement accuracy for FWXX, BWXX, FR00, FL00, BR00, BL00 
- We also need to test SNAP and FIN (so when STM finishes executing a sequence of strings and reach "SNAP", STM should send a message back to us,
then we take picture, once successful picture taken, we will send a message to STM saying continue the path)
- Therefore, its important that we can test a sequence of strings also
- In order to test this, we need scotch tape and ruler




# Standards/protocols for the message that will be transmitted across teams:

| is the message seperator
In general, a message will have a header aka what the message is for (TYPE) and some content.
A message will look like "TYPE|XXXXXX" - XXXX means the content,
————————————————————————————
@Android team, this is how the message should look like when you send to us:
"TASK1|[{'x':6,'y':2,'d':4}, {'x':4,'y':2,'d':0}, {'x':5,'y':2,'d':2}]" 
this message is for task 1 image rec, the header is TASK1, content is a list of dictionary with the coordinates and direction of obstacle.  @Algo team, this is the message you will receive also, so you will need to be able to interpret the message also.

"MANUAL|FR00" - this message is for the single manual movements for when you want to remote control the robot

————————————————————————————
@Algo team, when you finish processing the message with obstacles from Android, you're expecting to send us this message:
"TASK1|['FW10', 'FR00', 'FW70', 'BR00', 'BW20', 'SNAP', 'FW20', 'FIN']|[{'x':1,'y':1,'d':0, 's':0}, {'x':4,'y':2,'d':2. 's':0}, {'x':5,'y':2,'d':2, 's':1}]"
Header is TASK1, then | seperator, then first part of the message is a list of commands, then another | seperator, second part of message is the a list of  states where the robot should be when going through task 1, s represents screenshot if s:1, then robot will take screenshot there. 

@Android team, when we receive this message from algo, we will be sending you the part "[{'x':1,'y':1,'d':0, 's':0}, {'x':4,'y':2,'d':2, 's':0}, {'x':5,'y':2,'d':2, 's':1}]" of the message which is the locations of the robot, so you will need to setup to receive and interpret the message also. The way your simulator should work is, when you receive this message, you just continue waiting for more messages, when you receive a "NEXT" string from us, then you can assume the first location of the robot in the list is reached, and move your simulator robot as accordingly to the correct location.

If you receive a "FAIL" from us, assume there was some error and just show an error message.



————————————————————————————
@STM team, the message you will receive from us for task 1 is single messages e.g.
"FW10"
"FR00"
When you receive this message, you need to complete the given movement, once the movement is completed, then you need to send us an acknowledge message. Just send us "ACK" as a string.

————————————————————————————

# RPI:
## Multithreading:
Processes/Threads:

Each of the following represents a thread/process:
and each process will be running indefinitely using a while loop until program stops.

1. Receiving message from ANDROID
2. Receiving message from ALGO
3. Receiving message from STM
4. Sending message to ANDROID 
5. Sending message to ALGO
6. Sending message to STM
7. Taking picture for Image Rec

We will use four queues for storing the messages, in general, we receive message from the different external devices, 
determine what and who the message is for and store it in the designated team's queue.
The 4 queues are: toAndroidQueue, toAlgoQueue, toImgQueue, toSTMQueue

E.g. We receive message from android and realised the message is for ALGO, so we just push the message into ALGO's queue
Since all processes run at the same time, process (5) will see that the ALGO queue is not empty, and then send the message to ALGO.



below messages excludes like the statuses such as checking when STM32, ImageRec etc... are ready.
below are only for task 1 image rec, task 2 movement that include sensors etc are not included for now..

# Android
## Types of messages from Android
1. Android to Algo (obstacles and start message) - these messages might be seperate to allow time for calculation?
2. Android to STM (manually move)
3. Android to RPI (take picture?) then RPI take picture and send to Image Rec for processing.


## Functions for Android.py (via bluetooth)
1. __init__
2. connect
3. disconnect
4. send
5. receive

# Algo
## Types of messages from Algo
1. Algo to STM (movements for robot to take) e.g. STM, FW10, FR00, FW20, BL20... etc
2. Algo to Android (paths? like coordinates of robot so algo can simulate the run)


## Functions for Algo.py (via socket?)
1. __init__
2. connect
3. disconnect
4. send
5. receive

# STM32
## Types of messages from STM32
1. Reach designed location, ask RPI to take picture? Then RPI take pic and send to Image Rec to process before sending to Android the identified obstacle ID. (im not sure how this works)
2. Send message to say task completed



## Functions for STM32.py (via UART)
1. __init__
2. connect
3. disconnect
4. send
5. receive