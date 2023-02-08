

#testing STM32
from imagecapturefinal import ImageCapture

#testing android code
#from testingAndroid import MultiProcess

def init():
    try:
        print("Starting up group 6 rpi")

        image_capture = ImageCapture()
        image_capture.capture_and_detect()

    except KeyboardInterrupt:
        print("Keyboard interrupted, ending multiprocess")
    
    except Exception as error:
        print("Error has occured: ", error)



if __name__ == "__main__":
    init()
