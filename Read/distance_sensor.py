import RPi.GPIO as GPIO
import time
from datetime import datetime

def detect(t,e,s):
    GPIO.cleanup()
    try:
        GPIO.setmode(GPIO.BOARD)
        PIN_TRIGGER = t #7
        PIN_ECHO = e #11
        GPIO.setup(PIN_TRIGGER, GPIO.OUT)
        GPIO.setup(PIN_ECHO, GPIO.IN)

        GPIO.output(PIN_TRIGGER, GPIO.LOW)
        time.sleep(0.5)


        GPIO.output(PIN_TRIGGER, GPIO.HIGH)
        time.sleep(0.00001)
        GPIO.output(PIN_TRIGGER, GPIO.LOW)

        while GPIO.input(PIN_ECHO)==0:
            pulse_start_time = time.time()
        while GPIO.input(PIN_ECHO)==1:
            pulse_end_time = time.time()

        pulse_duration = pulse_end_time - pulse_start_time
        distance = round(pulse_duration * 17150, 2)
        time_current = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-2]
        return s, distance, time_current
       
    finally:
        GPIO.cleanup()