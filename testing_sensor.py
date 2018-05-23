import barometer  # online
import baro  # online merged with errno logic

sensor1 = barometer.barometer()
sensor2 = baro.barometer()

print(format("code", "<20s") +
        format("temperature", "<20s") + format("pressure", "<20s") + 
        format("altitude", "<20s") + format("converted", "<20s") + 
        format("correct pressure", "<20s"))

while(True):
    pressure1 = sensor1.getDigitalPressure()
    temperature1 = sensor1.getDigitalTemperature()
    converted1 = sensor1.convertPressureTemperature(pressur1, temperature1)
    pascal1 = sensor1.inHgToHectoPascal(29.95)
    altitude1 = sensor1.getMetricAltitude(converted, pascal1)
    print(format("code1", "<20s") +
            format("%0.2f" % temperature1, "<20s") +
            format("%0.2f" % pressure1, "<20s") +
            format("%0.2f" % altitude1, "<20s") +
            format("%0.2f" % converted1, "<20s") +
            format("---", "<20s")
            )

    sensor2.readBaro()
    print(format("code2", "<20s") + 
            format("%0.2f" % sensor2.getTemp(), "<20s") +
            format("%0.2f" % sensor2.getPressure(), "<20s") +
            format("%0.2f" % sensor2.getAltitude(), "<20s") +
            format("---", "<20s") +
            format("%0.2f" % sensor2.getCorrectPressure(), "<20s")
            )
