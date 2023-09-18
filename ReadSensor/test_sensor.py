import time
from gpiozero import DistanceSensor

# Initialize the sensors (ultrasonic sensors)
geton_sensor = DistanceSensor(echo=17, trigger=4)  # Connect the boarding sensor to GPIO 17 (echo) and GPIO 4 (trigger)
getoff_sensor = DistanceSensor(echo=18, trigger=5)  # Connect the alighting sensor to GPIO 18 (echo) and GPIO 5 (trigger)

# Initialize variables
current_passenger_count = 0
record_interval = 15  # Record data every 15 seconds
start_time = time.time()
time_list = []  # List to store time data
passenger_count_list = []  # List to store passenger count data

try:
    while True:
        # Listen for sensor events
        geton_distance = geton_sensor.distance
        if geton_distance <= 1.0:  # Set the threshold to 1 meter
            current_passenger_count += 1

        getoff_distance = getoff_sensor.distance
        if getoff_distance <= 1.0:  # Set the threshold to 1 meter
            current_passenger_count -= 1

        # Check if the recording interval has been reached
        elapsed_time = time.time() - start_time
        if elapsed_time >= record_interval:
            # Record the event
            current_time = time.strftime("%H:%M:%S", time.localtime())

            # Add time and passenger count to the lists
            time_list.append(current_time)
            passenger_count_list.append(current_passenger_count)

            # Reset the timer and passenger count
            start_time = time.time()

except KeyboardInterrupt:
    pass

# Output the results
print("Time List:", time_list)
print("Passenger Count List:", passenger_count_list)



