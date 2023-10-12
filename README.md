# CITS5506-GP40
## Topic - Smart Multi-purpose Passerby Counting System
This GitHub repository contains Python programs that must be stored in the Raspberry Pi 3 that will be used as the computing module to handle reading the detections from the connected sensors and implement any logic to calculate and update count values (which is done in logic.py when calling the ultrasonic sensors implementation of the system).

If the system is using ultrasonic sensors for detections, the count.py program must be run. Otherwise, if the laser distance sensors are used, laser_distance_sensor.py must be run.

## Group members:
- Rongchun Sun
- Yunwei Zhang
- Brandon Ke
- Aryan R.

### Steps to set up Software System
1. Power up the Raspberry Pi with Raspberry Pi 5VDC Power Supply plug, then connect it to a monitor with a HDMI cable.
1. Go to Menu > Programming > Thonny to open up the Thonny Python IDE on the Raspberry Pi.
3. Open count.py (bi-directional ultrasonic sensors version) or laser_distance_sensor.py (unidirectional laser distance sensors version).
4. (If running laser_distance_sensor.py) Follow these additional steps:
    - Open up a terminal.
    - Run the following command:
```
sudo pip3 install piicodev
```
4. Start running either of these programs for the system to start running and detecting.
