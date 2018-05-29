# this is a simple class for csv file creation and appending
# meant so that data can be opened as a spreadsheet

import os
import time

class csvFile:

    def __init__(self, directory = "./data/TSat_Files/", file_name = "data.csv"):
        self.path = directory + file_name
        
        if not os.path.exists(directory):
            os.makedirs(directory)

    def write(self, data):
        # TODO: need to do a little more research to determine whether we should open
        # and close the file every time we want to write, or if it would be okay to
        # just leave it open

        file_writing = open(self.path, "a")  # open to append
        file_writing.write(data)
        file_writing.write("\n")
        file_writing.close()
