# simple class to house code for the picamera

import os
import picamera
import subprocess
import time

class camera:

    def __init__(self, directory = "./data/TSat_Pics/"):
        # run subprocess to see if a camera is connected
        process = subprocess.Popen(["vcgencmd", "get_camera"],
                stdout=subprocess.PIPE)
        out, err = process.communicate()
        
        self.camera_connected = False
        if "detected=1" in out:
            self.camera_connected = True

        # if camera is connected, initialize camera
        if self.camera_connected:
            self.camera = picamera.PiCamera()
            self.dir = directory

        # if directory does not already exist, create it
        if not os.path.exists(directory):
            os.makedirs(directory)
        
    def takePicture(self):
        # take a picture if camera is connected
        if self.camera_connected:
            # done in case of restart
            self.camera.capture(self.dir + "image_" + str(int(time.time())) + ".jpg")
