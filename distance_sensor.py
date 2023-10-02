import RPi.GPIO as GPIO
import time
from datetime import datetime

TRIGGER1 = 7
TRIGGER2 = 29
ECHO1 = 11
ECHO2 = 35

def detect():
    #GPIO.cleanup()
    try:
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(TRIGGER1, GPIO.OUT)
        GPIO.setup(ECHO1, GPIO.IN)
        GPIO.setup(TRIGGER2, GPIO.OUT)
        GPIO.setup(ECHO2, GPIO.IN)

        GPIO.output(TRIGGER1, GPIO.LOW)
        time.sleep(0.5)


        GPIO.output(TRIGGER1, GPIO.HIGH)
        GPIO.output(TRIGGER2, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(TRIGGER1, GPIO.LOW)
        GPIO.output(TRIGGER2, GPIO.LOW)

        pulse_start_time1 = 0
        pulse_start_time2 = 0
        pulse_end_time1 = 0
        pulse_end_time2 = 0

        while pulse_start_time1 <= 0 or pulse_start_time2 <= 0:
            if GPIO.input(ECHO1) == 1 and pulse_start_time1 <= 0:
                pulse_start_time1 = time.time()
            if GPIO.input(ECHO2) == 1 and pulse_start_time2 <= 0:
                pulse_start_time2 = time.time()
        while pulse_end_time1 <= 0 or pulse_end_time2 <= 0:
            if GPIO.input(ECHO1) == 0 and pulse_end_time1 <= 0:
                pulse_end_time1 = time.time()
            if GPIO.input(ECHO2) == 0 and pulse_end_time2 <= 0:
                pulse_end_time2 = time.time()

        pulse_duration1 = pulse_end_time1 - pulse_start_time1
        distance1 = round(pulse_duration1 * 17150, 2)

        pulse_duration2 = pulse_end_time1 - pulse_start_time1
        distance2 = round(pulse_duration2 * 17150, 2)

        time_current = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-2]
        return distance1, distance2, time_current
       
    finally:
        GPIO.cleanup()
        #print(distance)
        #return s, distance, time_current
        
#detect(7,11,"11")