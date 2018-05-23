# MS5607
# https://github.com/llinear/MS5607/blob/master/MS5607.py

import math
import smbus
import time

bus = smbus.SMBus(1)

class barometer:

    DEVICE_ADDRESS = 0x76

    _CMD_RESET = 0x1E
    _CMD_ADC_READ = 0x00
    _CMD_PROM_RD = 0xA0
    _CMD_ADC_CONV = 0x40

    _CMD_ADC_D1 = 0x00
    _CMD_ADC_D2 = 0x10

    _CMD_ADC_256 = 0x00
    _CMD_ADC_512 = 0x02
    _CMD_ADC_1024 = 0x04
    _CMD_ADC_2048 = 0x06
    _CMD_ADC_4096 = 0x08

    def __init__(self):
        self.resetSensor()
        self.coefficients = self.readCoefficients()

    # UTILITY METHODS
    def read16U(self, register):
        bytes = bus.read_i2c_block_data(self.DEVICE_ADDRESS, register, 2)
        return (bytes[0] << 8) + (bytes[1])

    def read24U(self, register):
        bytes = bus.read_i2c_block_data(self.DEVICE_ADDRESS, register, 3)
        return (bytes[0] << 16) + (bytes[1] << 8) + (bytes[2])

    def hectoPascalToInHg(self, milliBar):
        return milliBar * 29.5333727 / 100000

    def inHgToHectoPascal(self, inHg):
        return 100000 * inHg / 29.5333727

    def getImperialAltitude(self, currentMilliBar, baseMilliBar):
        return (1 - math.pow(currentMilliBar / baseMilliBar, 0.190284)) * 145366.45

    def getMetricAltitude(self, currentMilliBar, baseMilliBar):
        return 0.3048 * self.getImperialAltitude(currentMilliBar, baseMilliBar)

    # COMMANDS
    def resetSensor(self):
        bus.write_byte(self.DEVICE_ADDRESS, self._CMD_RESET)
        time.sleep(0.003)  # wait for reset sequence

    def readCoefficient(self, i):
        return self.read16U(self._CMD_PROM_RD + 2 * i, self._CMD_PROM_RD + 2 *
                i + 1)

    def readCoefficients(self):
        coefficients = [0] * 6
        for i in range(6):
            coefficients[i] = self.readCoefficient(i + 1)
        return coefficients

    def readAdc(self, cmd):
        bus.write_byte(self.DEVICE_ADDRESS, self._CMD_ADC_CONV + cmd)
        sleepTime = {self._CMD_ADC_256: 0.0009,
                self._CMD_ADC_512: 0.003,
                self._CMD_ADC_1024: 0.004,
                self._CMD_ADC_2048: 0.006,
                self._CMD_ADC_4096: 0.010 }
        time.sleep(sleepTime[cmd & 0x0f])
        return self.read24U(self._CMD_ADC_READ)

    def getDigitalPressure(self):
        return self.readAdc(self._CMD_ADC_D1 + self._CMD_ADC_4096)

    def getDigitalTemperature(self):
        return self.readAdc(self._CMD_ADC_D2 + self._CMD_ADC_4096)

    def getTemperature(self):
        dT = self.getDigitalTemperature() - self.coefficients[4] * math.pow(2,8)
        return (2000 + dT * self.coefficients[5] / math.pow(2,23)) / 100

    def convertPressureTemperature(self, pressure, temperature):
        dT = temperature - self.coefficients[4] * 256
        offset = self.coefficients[1] * 4 + ((float(dT) / 2048) *
            (float(self.coefficients[3]) / 1024))
        sens = self.coefficients[0] * 2 + ((float(dT) / 4096) *
            (float(self.coefficients[2]) / 1024))
        press = (float(pressure) / 2048) * (float(sens) / 1024) - offset
        return press
