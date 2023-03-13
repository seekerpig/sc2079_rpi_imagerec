# sc2079_rpi_imagerec
Github repository for SC2079 RPI and Image Rec - Group 06


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


## Functions for Algo.py (via socket)
1. __init__
2. connect
3. disconnect
4. send
5. receive

# STM32
## Types of messages from STM32
1. Reach designed location, ask RPI to take picture? Then RPI take pic and send to Image Rec to process before sending to Android the identified obstacle ID. (im not sure how this works)
2. Send message to say task completed



## Functions for STM32.py (via UART/serial)
1. __init__
2. connect
3. disconnect
4. send
5. receive
