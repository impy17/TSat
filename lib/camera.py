# simple class to house code for the picamera

import picamera
from time import time

class camera:

    def __init__(self, directory = "./TSat_Pics/"):
        self.camera = picamera.PiCamera()
        self.dir = directory
        
    def takePicture(self):
        self.camera.capture(self.dir + str(time()).replace(".", "") + ".jpg")
