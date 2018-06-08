# this file is inteded to run on startup, so make sure to add it as a daemon

# TODO: error handling
import sys

import RPi.GPIO as GPIO

from lib.camera import camera
from lib.clock import clock
from lib.csv_file import csvFile
from lib.barometer import barometer
from lib.median_filter import filter
from time import sleep
from time import time

# constant values
RESERVED  = 7   # number of values for median filter
LO_PRES   = 5   # for pressure range, low value, 5 for flight
HI_PRES   = 12  # for pressure range, high value, 12 for flight
TIME      = 60  # in seconds, for picture taking delay
DATA_SMPL = 2   # length in seconds between data samples
LED_DELAY = 30  # length of time the status LED stays on

# constant gpio pin numbers
SWITCH_PIN = 12  # board pin 32, boom switch
LED_PIN    = 20  # board pin 38, led light
WIREC_PRIM = 23  # board pin 16, primary wire cutter
WIREC_SECD = 24  # board pin 18, secondary wire cutter
BUCK_CONVT = 25  # board pin 22, buck converter

# constant status strings
CMR_IMAGED = "CMR_IMGD"  # picam took a picture
CMR_FAILED = "CMR_FAIL"  # picam not connected properly, failed to take picture
BOM_DEPLOY = "BOM_DPLY"  # boom deployed
BOM_FAILED = "BOM_FAIL"  # boom did not deploy

# initialization of components
try:
    med_filter  = filter(RESERVED)
    pi_camera   = camera()
    baro_sensor = barometer()
    elapsed_clk = clock()
    data_file   = csvFile()

except:
    print("Error during constructors:", sys.exc_info()[0])
    sys.exit(1)

# initialization of GPIO pins
try:
    GPIO.setmode(GPIO.BCM)  # use GPIO pin numbers

    # GPIO outputs
    GPIO.setup(LED_PIN, GPIO.OUT, initial=0)
    GPIO.setup(WIREC_PRIM, GPIO.OUT, initial=0)
    GPIO.setup(WIREC_SECD, GPIO.OUT, initial=0)
    GPIO.setup(BUCK_CONVT, GPIO.OUT, initial=0)

    # GPIO inputs
    GPIO.setup(SWITCH_PIN, GPIO.IN)

except:
    print("Error during GPIO setup: ", sys.exc_info()[0])
    sys.exit(1)

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

# If we get to this point, most error-prone initialization should
# have taken place. Turn on status LED for a little bit,
# then start the main loop.
GPIO.output(LED_PIN, GPIO.HIGH)
sleep(LED_DELAY)
GPIO.output(LED_PIN, GPIO.LOW)

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
        # if the boom switch is closed
        # 1. write high to the buck converter
        # 2. write high to primary wire cutter and wait a second
        # 3. check if boom switch reads open
        # 4. if not open, write high to secondary wire cutter and wait
        # 5. check if boom switch reads open
        # 6. write status report to file
        if boom_switch == 0:  # if closed
            GPIO.output(BUCK_CONVT, GPIO.HIGH)
            GPIO.output(WIREC_PRIM, GPIO.HIGH)
            sleep(2)
            GPIO.output(WIREC_PRIM, GPIO.LOW)
            boom_switch = GPIO.input(SWITCH_PIN)
            if boom_switch == 0:  # if still closed
                GPIO.output(WIREC_SECD, GPIO.HIGH)
                sleep(2)
                GPIO.output(WIREC_SECD, GPIO.LOW) 
                boom_switch = GPIO.input(SWITCH_PIN) 
            GPIO.output(BUCK_CONVT, GPIO.LOW)
            if boom_switch == 0:  # if still closed
                status = BOM_FAILED
            else:
                status = BOM_DEPLOY
                take_picture = True
            output =  format("%8s " % status + "\t")
            print(output)  # NOTE: only for testing purposes
            data_file.write(output)

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

    if boom_switch == 1:  # NOTE: will read 0 if switch not connected
        output += format("%8s " % "open" + "\t")
    else:
        output += format("%8s " % "closed" + "\t")

    # logging to file
    print(output)  # NOTE: only for testing purposes
    data_file.write(output)

    # waithing DATA_SMPL seconds before resampling
    sleep(DATA_SMPL)
