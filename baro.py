# MS5607

import math
import smbus
import time

bus = smbus.SMBus(1)

class barometer:

    DEVICE_ADDRESS = 0x76

    _CMD_RESET = 0x1E
    _CMD_PROM_RD = 0xA0  # 0xA2 ?

    def __init__(self):
        self.resetSensor()

        self.D1 = 0
        self.D2 = 0
        self.dT = 0
        self.temp = 0
        self.off = 0
        self.sens = 0
        self.pres = 0
        self.coeff = self.readCoefficients()

        self.temperature = 0
        self.pressure = 0
        self.correct_pressure = 0
        self.altitude = 0
        self.tempKelvin = 0

    def resetSensor(self):
        bus.write_byte(self.DEVICE_ADDRESS, self._CMD_RESET)
        time.sleep(0.003)  # wait for reset sequence

    def read16U(self, register):
        bytes = bus.read_i2c_block_data(self.DEVICE_ADDRESS, register, 2)
        return (bytes[0] << 8) + (bytes[1])

    def readCoefficient(self, i):
        return self.read16U(self._CMD_PROM_RD + (i * 2))

    def readCoefficients(self):
        coefficients = [0] * 6
        for i in range(6):
            coefficients[i] = self.readCoefficient(i + 1)
        return coefficients

    def getVal(self, code):
        bus.write_byte(self.DEVICE_ADDRESS, code)
        time.sleep(10)  # delay(10) in errno code

        bus.write_byte(self.DEVICE_ADDRESS, 0x00)

        '''
        equivalent to:
        Wire.beginTransmission(address);
        Wire.requestFrom(address, (int)3);
        if (Wire.available() >= 3)
            ret = Wire.read() * (unsigned long)65536 + Wire.read() *
                (unsigned long)256 + Wire.read();
        else
            ret = -1;
        Wire.endTransmission();
        return ret;
        '''

    def readBaro(self):
        self.D1 = self.getVal(0x48)  # raw pressure, 0x00?
        self.D2 = self.getVal(0x58)  # raw temperature, 0x10?

        self.dT = self.D2 - (float(self.coeff[5]) * math.pow(2, 8))
        self.off = (float(self.coeff[2]) * math.pow(2,17)) + ((self.dT *
            self.coeff[4]) / math.pow(2, 6))
        self.sens = (float(self.coeff[1]) * math.pow(2,16)) + ((self.dT *
            self.coeff[3]) / math.pow(2, 7))
        self.temp = 2000 + float(self.dT) * float(self.coeff[6]) / math.pow(2, 23)

        if (self.temp < 2000):
            t1 = math.pow(self.dT, 2) / math.pow(2, 31)
            off1 = 61 * math.pow((self.temp - 2000), 2) / math.pow(2, 4)
            sens1 = 2 * math.pow((self.temp - 2000), 2)

            if (self.temp < -1500):
                off1 = off1 + 15 * math.pow((self.temp + 1500), 2)
                sens1 = sens1 + 8 * math.pow((self.temp + 1500), 2)

            self.temp -= t1
            self.off -= off1
            self.sens -= sens1

        self.temperature = float(self.temp) / 100
        self.pres = (float(self.D1) * self.sens / math.pow(2, 21) - self.off)/math.pow(2, 15) 
        self.pressure = float(self.pres) / 100
        self.tempKelvin = self.temperature + 273.15

        self.altitude = (1 - math.pow((self.pressure / 1013.25), 0.190264))*44330.76923

        self.correct_pressure = (self.pressure / math.exp((-self.altitude /
            (self.tempKelvin * 29.263))))

        self.altitude = self.altitude * 3.2808

    def getTemp(self):
        return self.temperature

    def getPressure(self):
        return self.pressure

    def getAltitude(self):
        return self.altitude

    def getCorrectPressure(self):
        return self.correct_pressure

