# TSat

Tiny-Sat (TSat) is a minimalistic satellite prototype designed to be tested on high altitude balloons (HABs).  Any available information about TSat and its parents can be found on Utah State University's official Get Away Special Team's [website](https://getawayspecial.usu.edu "USU GAS Team").

In summary, the primary purpose of TSat is to deploy a meter long passive stabilization device named the "Aeroboom".  Upon deployment, the Aeroboom will inflate in the low pressure and harden into a cylidrical shape due to a UV-curing epoxy.  The primary goal of TSat is the deployment and of this Aeroboom.

## Experiment Design

TSat consists of a Raspberry Pi Uno, a Raspberry Pi camera, an MS5607 Parallax Altimeter, two wire cutters, and a box containing the folded Aeroboom.  The MS5607 sensor can read barometric pressure.  By employing the logic of a median filter to smooth out any outlier sensor readings, the code is designed to deploy the boom when the HAB payload rises into a specified pressure range.  A signal is sent to the two wire cutters, a primary and a secondary, which will then cut through the wires tying the boom box closed, allowing the Aeroboom to inflate.  When the Aeroboom deploys, the picamera will begin taking documentary pictures.  Throughout the process, the sensor readings will also be saved to the Raspberry Pi for later study.
