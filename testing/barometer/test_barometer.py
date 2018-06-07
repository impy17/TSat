# testing code for barometers

from barometer import barometer
import time

logger = file("log.txt", "a")

baro_sensor = barometer()

while True:
    baro_sensor.readBaro()
    pressure = baro_sensor.getPressure()
    tempC    = baro_sensor.getTemperatureC()
    tempF    = baro_sensor.getTemperatureF()
    altitude = baro_sensor.getAltitude(pressure)

    output =  format("Pressure (in millibars): %.2f" % pressure, "<35s")
    output += format("Altitude: %.2f" % altitude, "<20s")
    output += format("TempC: %.2f" % tempC, "<20s")
    output += format("TempF: %.2f" % tempF, "<20s")
    print(output)
    logger.write(output)
    logger.write("\n")

    time.sleep(1)
