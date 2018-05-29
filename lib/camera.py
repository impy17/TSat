# simple class to house code for the picamera

import os
import picamera
import time

class camera:

    def __init__(self, directory = "./data/TSat_Pics/"):
        self.camera = picamera.PiCamera()
        self.dir = directory

        if not os.path.exists(directory):
            os.makedirs(directory)
        
    def takePicture(self):
        # done in case of restart
        self.camera.capture(self.dir + "image_" + str(int(time.time())) + ".jpg")
