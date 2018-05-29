# this file is inteded to run on startup, so make sure to add it as a daemon

# TODO: handling errors

from lib.camera import camera
from lib.clock import clock
from lib.barometer import barometer
from lib.median_filter import filter
from time import sleep
from time import time

# constants
RESERVED = 7  # number of values for median filter
LO_PRES = 15  # for pressure range, low value
HI_PRES = 35  # for pressure range, high value
TIME = 60     # in seconds, for picture taking delay

# initialization of components
med_filter  = filter(RESERVED)
pi_camera   = camera()
baro_sensor = barometer()
elapsed_clk = clock()

# opening file
data = file("data/data.txt", "w")

# some helper variables for image taking
take_picture  = False
elapsed_time  = TIME
previous_time = 0

# initial output
output = ""
output += format("Pressure", "<10s")
output += format("TempC", "<10s")
output += format("TempF", "<10s")
output += format("Altitude", "<10s")
output += format("Time", "<10s")

# TODO: currently printing to console, but need to print to a tabbed file
print(output)
data.write(output)

# a forever loop that constantly reads and handles data
# 1. barometer values are read and correct pressure is added to median filter
# 2. new output is displayed and saved to correct file
# 3. if pressure is in correct range, boom is deployed
# 4. if boom was deployed, picture is taken every TIME miliseconds
while True:
    baro_sensor.readBaro()
    med_filter.add(baro_sensor.getPressure())
    elapsed_clk.readTime()

    output = ""
    output += format("%.2f " % baro_sensor.getPressure(), "<10s")
    output += format("%.2f " % baro_sensor.getTemperatureC(), "<10s")
    output += format("%.2f " % baro_sensor.getTemperatureF(), "<10s")
    output += format("%.2f " % baro_sensor.getAltitude(), "<10s")
    output += format("%02d:%02d:%02d" % (elapsed_clk.getHours(),
            elapsed_clk.getMinutes(),
            elapsed_clk.getSeconds()),
            "<10s")

    # TODO: currently printing to console, but need to print to a tabbed file
    print(output)
    data.write(output)

    # determine boom deployment time
    median = med_filter.median()
    if median <= HI_PRES and median >= LO_PRES:
        # TODO: send high to wire cutters
        take_picture = True

    # determine picture taking time
    if take_picture:
        if elapsed_time >= TIME:
            elapsed_time = 0
            pi_camera.takePicture()
            previous_time = time()
        else:
            current_time = time()
            elapsed_time += current_time - previous_time
            previous_time = current_time

    sleep(2)  # sleep for 1 second
