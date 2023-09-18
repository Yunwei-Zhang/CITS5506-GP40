import time
from gpiozero import DistanceSensor

# Initialize the sensors (ultrasonic sensors)
No1_sensor = DistanceSensor(echo=17, trigger=4)  # Connect the first sensor to GPIO 17 (echo) and GPIO 4 (trigger)
No2_sensor = DistanceSensor(echo=18, trigger=5)  # Connect the second sensor to GPIO 18 (echo) and GPIO 5 (trigger)

# Initialize variables
current_passenger_count = 0
record_interval = 15  # Record data every 15 seconds
start_time = time.time()
time_list = []  # List to store time data
passenger_count_list = []  # List to store passenger count data

# Initialize a state variable to track the current state
# 0 - No one is passing, 1 - Someone is passing from Sensor 1 to Sensor 2, 2 - Someone is passing from Sensor 2 to Sensor 1
state = 0

try:
    while True:
        # Listen for sensor events
        No1_distance = No1_sensor.distance
        No2_distance = No2_sensor.distance

        # Check if someone is entering from Sensor 1 to Sensor 2
        if state == 0:
            if No1_distance <= 1.0:
                state = 1
        elif state == 1:
            if No2_distance <= 1.0:
                current_passenger_count += 1
                state = 0

        # Check if someone is exiting from Sensor 2 to Sensor 1
        if state == 0:
            if No2_distance <= 1.0:
                state = 2
        elif state == 2:
            if No1_distance <= 1.0:
                current_passenger_count -= 1
                state = 0

        # Check if the recording interval has been reached
        elapsed_time = time.time() - start_time
        if elapsed_time >= record_interval:
            # Record the event
            current_time = time.strftime("%H:%M:%S", time.localtime())

            # Add time and passenger count to the lists
            time_list.append(current_time)
            passenger_count_list.append(current_passenger_count)

            # Reset the timer
            start_time = time.time()

        # Sleep for a short time to avoid high CPU usage
        time.sleep(0.1)

except KeyboardInterrupt:
    pass

# Output the results
print("Time List:", time_list)
print("Passenger Count List:", passenger_count_list)
