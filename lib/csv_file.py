# this is a simple class for csv file creation and appending
# meant so that data can be opened as a spreadsheet

import os

class csv_file:

    def __init__(self, directory = "../data/", file_name = "data.csv"):
        self.path = directory + file_name
        
        if not os.path.exists(directory):
            os.makedirs(directory)

    def write(self, data):
        file_writing = open(self.path, "a")
        file_writing.write(data)
        file_writing.write("\n")
        file_writing.close()
