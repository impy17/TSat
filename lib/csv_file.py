# this is a simple class for csv file creation and appending
# meant so that data can be opened as a spreadsheet

import os


class csvFile:
    def __init__(self, directory="./data/TSat_Files/", file_name="data.csv"):
        self.path = directory + file_name

        if not os.path.exists(directory):
            try:
                os.makedirs(directory)
            except OSError as e:
                print(e)
                raise

        try:
            self.file = open(self.path, "a")  # open to append
        except IOError as e:
            print(e)
            raise

    def __del__(self):
        self.file.close()

    def write(self, data):
        self.file.write(data)
        self.file.write("\n")
