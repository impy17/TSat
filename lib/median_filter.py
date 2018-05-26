# simple class to house code for median filter

import math

class filter:

    def __init__(self, reserved):
        self.data = [None] * reserved
        self.sorted = []
        self.reserved = reserved

    # adding a value
    def add(self, value):
        if len(self.data) == self.reserved:
            self.data.pop(0)
        self.data.append(value)

    # retrieving median value
    def median(self):
        self.sorted = []

        for i in range(self.reserved):
            if self.data[i] != None:
                self.sorted.append(self.data[i])

        self.sorted.sort()
        middle = math.floor(len(self.sorted) / 2)
        return self.sorted[middle]
