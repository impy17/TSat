# simple class to house code for clock

import time

class clock:

    def __init__(self):
        self.base_time = int(time.time())
        self.elapsed_time = int(time.time())
        self.seconds = 0
        self.minutes = 0
        self.hours = 0

    def readTime(self):
        self.elapsed_time = int(time.time()) - self.base_time
        remaining_seconds = self.elapsed_time
        
        self.hours = int(remaining_seconds / (60 * 60))
        remaining_seconds -= int(self.hours * 60 * 60)
        self.minutes = int(remaining_seconds / 60)
        self.seconds = int(remaining_seconds % 60)

    def getSeconds(self):
        return self.seconds

    def getMinutes(self):
        return self.minutes

    def getHours(self):
        return self.hours
