# code adapted for the MS5607 from
# https://github.com/ControlEverythingCommunity/MS5803-02Ba/blob/master/Python/MS5803_02BA.py

# NOTE:
# potential altitude calculation would be difficult as most formulas
# require calculation of a sea-level reference based on current
# atmospheric conditions, such that the sensor's code would have to be
# recalibrated whenever the weather changes; a rough estimate could
# potentially be achieved, but such a venture will not be persued at
# this time

import math
import smbus
import time

bus = smbus.SMBus(1)

class barometer:

    DEVICE_ADDRESS = 0x76

    def __init__(self):
        self.resetCommand()

        self.dT     = 0
        self.TEMP   = 0
        self.OFF    = 0
        self.SENS   = 0 
        self.C      = self.readCalibrations()

        self.pressure = 0  # in millibars
        self.tempC    = 0  # in degrees C
        self.tempF    = 0  # in degrees F

    def readBaro(self):
        # read digital pressure value
        pressureConversionCommand()
        self.D1 = readDigitalValue()

        # read digital temperature value
        temperatureConversionCommand()
        self.D2 = readDigitalValue()

        # calculations
        self.dT   = self.D2 - self.C[5] * 256
        self.TEMP = 2000 + self.dT * self.C[6] / 8388608
        self.OFF  = self.C[2] * 131072 + (self.C[4] * self.dT) / 64
        self.SENS = self.C[1] * 65536 + (self.C[3] * self.dT) / 128

        TEMP2 = 0
        OFF2  = 0
        SENS2 = 0

        if self.TEMP < 2000:
            TEMP2 = (self.dT * self.dT) / 2147483648
            OFF2  = 61 * ((self.TEMP - 2000) ** 2) / 16
            SENS2 = 2 * ((self.TEMP - 2000) ** 2)
            if self.TEMP < -1500:
                OFF2  = OFF2 + 20 * ((self.TEMP + 1500) ** 2)
                SENS2 = SENS2 + 12 * ((self.TEMP + 1500) ** 2)

        self.TEMP -= TEMP2
        self.OFF  -= OFF2
        self.SENS -= SENS2

        self.pressure = ((((self.D1 * self.SENS) / 2097152) - self.OFF) / 32768.0) / 100.0
        self.tempC    = self.TEMP / 100.0
        self.tempF    = self.tempC * 1.8 + 32

    # UTILITY FUNCTIONS
    def readCalibrations(self): 
        coefficients = [] * 6
        
        # pressure sensitivity
        coefficients[0] = readCalibration(0xA2)

        # pressure offset
        coefficients[1] = readCalibration(0xA4)

        # temperature coefficient of pressure sensitivity
        coefficients[2] = readCalibration(0xA6)

        # temperature coefficient of pressure offset
        coefficients[3] = readCalibration(0xA8)

        # reference temperature
        coefficients[4] = readCalibration(0xAA)

        # temperature coefficient of temperature
        coefficients[5] = readCalibration(0xAC)

        return coefficients

    def readCalibration(self, coefficent):
        data = bus.read_i2c_block_data(DEVICE_ADDRESS, coefficient, 2)
        return data[0] * 256 + data[1]

    def readDigitalValue(self):
        value = bus.read_i2c_block_data(DEVICE_ADDRESS, 0x00, 3)
        return value[9] * 65536 + value[1] * 256 + value[2]

    def resetCommand(self):
        bus.write_byte(DEVICE_ADDRESS, 0x1E)
        time.sleep(0.003)

    def pressureConversionCommand(self):
        bus.write_byte(DEVICE_ADDRESS, 0x40)
        time.sleep(0.003)

    def temperatureConversionCommand(self):
        bus.write_byte(DEVICE_ADDRESS, 0x50)
        time.sleep(0.003)

    # GETTER FUNCTIONS
    def getPressure(self):
        return self.pressure

    def getTemperatureC(self):
        return self.tempC

    def getTemperatureF(self):
        return self.tempF
