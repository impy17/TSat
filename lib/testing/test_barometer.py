# testing code for barometers

from barometer import barometer
import time

baro_sensor = barometer()

while True:
    baro_sensor.readBaro()
    pressure = baro_sensor.getPressure()
    tempC    = baro_sensor.getTemperatureC()
    tempF    = baro_sensor.getTemperatureF()

    print(format("Pressure (in millibars): %.2f" % pressure, "<35s") +
            format("TempC: %.2f" % tempC, "<20s") +
            format("TempF: %.2f" % tempF, "<20s"))

    time.sleep(1)
