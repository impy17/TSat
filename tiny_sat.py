# this file is inteded to run on startup, so make sure to add it as a daemon

# TODO: error handling

import RPi.GPIO as GPIO

from lib.camera import camera
from lib.clock import clock
from lib.csv_file import csvFile
from lib.barometer import barometer
from lib.median_filter import filter
from time import sleep
from time import time

# constant values
RESERVED = 7  # number of values for median filter
LO_PRES = -1  # for pressure range, low value  # TODO: 15 for flight
HI_PRES = 860  # for pressure range, high value  # TODO: 35 for flight
TIME = 60     # in seconds, for picture taking delay
DATA_SMPL = 2  # length in seconds between data samples

# constant gpio pin numbers
SWITCH_PIN = 18  # board pin 12

# constant status strings
CMR_IMAGED = "CMR_IMGD"  # picam took a picture
CMR_FAILED = "CMR_FAIL"  # picam not connected properly, failed to take picture
BOM_DEPLOY = "BOM_DPLY"  # boom deployed
BOM_FAILED = "BOM_FAIL"  # boom did not deploy

# initialization of components
med_filter  = filter(RESERVED)
pi_camera   = camera()
baro_sensor = barometer()
elapsed_clk = clock()
data_file   = csvFile()

# TODO: set up correct pin numbers
# TODO: arbitrary pins currently selected
# all GPIO ports have a 3.3V high and 0V low on GPIO.OUT
# there is no definable voltage on GPIO.IN
GPIO.setmode(GPIO.BCM)  # use GPIO pin numbers

# OUTPUTS - for wire cutters
# GPIO.setup(17, GPIO.OUT, initial=0)  # primary wire cutter, board pin 11, initial low
# GPIO.setup(27, GPIO.OUT, initial=0)  # secondary wire cutter, board pin 13, initial low
# GPIO.output(port_or_pin, 1)  # set high
# GPIO.output(port_or_pin, 0)  # set low

# INPUTS
GPIO.setup(SWITCH_PIN, GPIO.IN)

# some helper variables for image taking
take_picture  = False
elapsed_time  = TIME
previous_time = 0

# initial output
output =  format("  Status" + "\t")
output += format("Pressure" + "\t")
output += format("   TempC" + "\t")
output += format("   TempF" + "\t")
output += format("Altitude" + "\t")  # change in altitude from first sampling
output += format("    Time" + "\t")  # increment of time starting at 00:00:00
output += format("  Switch" + "\t")

# logging to file
print(output)  # NOTE: only for testing purposes
data_file.write(output)

# a forever loop that constantly reads and handles data
# 1. barometer values are read and correct pressure is added to median filter
# 2. new output is displayed and saved to correct file
# 3. if pressure is in correct range, boom is deployed
# 4. if boom was deployed, picture is taken every TIME seconds
# 5. wait DATA_SMPL seconds before sampling data again
while True:
    # status string
    status = ""

    # reading from components
    baro_sensor.readBaro()
    med_filter.add(baro_sensor.getPressure())
    elapsed_clk.readTime()

    # read boomswitch open/closed
    boom_switch = GPIO.input(SWITCH_PIN)

    # get median
    median = med_filter.median()

    # determine boom deployment time
    if median <= HI_PRES and median >= LO_PRES:
        # TODO: handle wire cutting, update boom switch, and log status
        take_picture = True

    # determine picture taking time
    if take_picture:
        if elapsed_time >= TIME:
            elapsed_time = 0
            # log if camera fails to take picture
            if pi_camera.takePicture():
                status = CMR_IMAGED
            else:
                status = CMR_FAILED
            previous_time = time()
        else:
            current_time = time()
            elapsed_time += current_time - previous_time
            previous_time = current_time

    # determine output values
    output =  format("%8s " % status + "\t")
    output += format("%8.2f " % baro_sensor.getPressure() + "\t")
    output += format("%8.2f " % baro_sensor.getTemperatureC() + "\t")
    output += format("%8.2f " % baro_sensor.getTemperatureF() + "\t")
    output += format("%8.2f " % baro_sensor.getAltitude(median) + "\t")
    output += format("%02d:%02d:%02d" % (elapsed_clk.getHours(),
            elapsed_clk.getMinutes(),
            elapsed_clk.getSeconds()) + "\t")

    if boom_switch == 0:
        output += format("%8s " % "open" + "\t")
    else:
        output += format("%8s " % "closed" + "\t")

    # logging to file
    print(output)  # NOTE: only for testing purposes
    data_file.write(output)

    # waithing DATA_SMPL seconds before resampling
    sleep(DATA_SMPL)
