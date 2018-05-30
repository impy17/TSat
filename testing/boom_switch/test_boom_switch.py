# test for boom switch readings
# NOTE: might have to run as sudo to access GPIO pins

# REFERENCE:
# https://www.cl.cam.ac.uk/projects/raspberrypi/tutorials/robot/buttons_and_switches/

# COMPONENTS:
# 1. the switch
# 2. 1k resistor
# 3. 10k resistor

# CIRCUIT DESIGN v1:
# 1. one side of the switch is connected directly to GND (ground)
# 2. other side of switch connects to a branching node
# 3. one branch goes to GPIO pin with 1k resistor in series
# 4. other branch goes to 3.3V with 10k resistor in series

# CIRCUIT DESIGN v2:
# 1. one side of the switch is connected directly to 3.3V
# 2. other side of switch connects to a branching node
# 3. one branch goes to GPIO pin with 1k resistor in series
# 4. other branch goes to GND with 10k resistor in series

import RPi.GPIO as GPIO
import time

# constants
SWITCH_PIN = 18

# GPIO initialization
GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH_PIN, GPIO.IN)

# infinite loop
while True:
    input = GPIO.input(SWITCH_PIN)

    if input == 0:
        print("open")
    else:
        print("closed")

    time.sleep(1)  # wait a second between readings
