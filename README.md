# sc2079_rpi_imagerec
Github repository for SC2079 RPI and Image Rec - Group 06

##TODOS:
- We need to figure out what kind of messages each team will send to each other
- We need to define how those messages should look like. 
- Figure out camera height versus obstacle height, then start taking photos


Example:    {
                'target': target, (e.g. "ALGO")
                'payload': message,
            }


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


