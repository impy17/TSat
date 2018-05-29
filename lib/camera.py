# simple class to house code for the picamera

import os
import picamera
from time import time

class camera:

    def __init__(self, directory = "./data/TSat_Pics/"):
        self.camera = picamera.PiCamera()
        self.dir = directory
        self.count = 0

        if not os.path.exists(directory):
            os.makedirs(directory)
        
    def takePicture(self):
        self.camera.capture(self.dir + "image_" + str(self.count) + ".jpg")
        self.count += 1
