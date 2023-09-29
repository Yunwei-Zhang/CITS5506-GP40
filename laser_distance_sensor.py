from PiicoDev_VL53L1X import PiicoDev_VL53L1X
from datetime import datetime

# Install piicodev package on Thonny on RaspberryPi
sensor = PiicoDev_VL53L1X()

def detect(t,e,s):
    # Record distance and convert to cm
    distance = sensor.read()
    distance = distance * 10

    time_current = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-2]
    return s, distance, time_current
       

#detect(7,11,"11")