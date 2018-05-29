# simple class to house code for the picamera

import picamera
from time import time

class camera:

    def __init__(self, directory = "./TSat_Pics/"):
        self.camera = picamera.PiCamera()
        self.dir = directory
        self.count = 0
        
    def takePicture(self):
        self.camera.capture(self.dir + "image_" + str(self.count) + ".jpg")
        self.count += 1
