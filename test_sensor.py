import time
from gpiozero import Button

def readFromSensor():     
    # Initialize the sensors (buttons)
    geton_sensor = Button(17)   # Connect the boarding sensor to GPIO 17
    getoff_sensor = Button(18)  # Connect the alighting sensor to GPIO 18

    # Initialize variables
    current_passenger_count = 0
    record_interval = 15  # Record data every 15 seconds
    start_time = time.time()
    time_list = []  # List to store time data
    passenger_count_list = []  # List to store passenger count data

    try:
        while True:
            # Listen for sensor events
            geton_sensor.wait_for_press()
            current_passenger_count += 1
            getoff_sensor.wait_for_press()
            current_passenger_count -= 1

            # Check if the recording interval has been reached
            elapsed_time = time.time() - start_time
            if elapsed_time >= record_interval:
                # Record the event
                current_time = time.strftime("%H:%M:%S", time.localtime())
                #print(f"Time: {current_time}, Passenger Count: {current_passenger_count}")

                # Add time and passenger count to the lists
                time_list.append(current_time)
                passenger_count_list.append(current_passenger_count)

                # Reset the timer and passenger count
                start_time = time.time()
                #current_passenger_count = 0

    except KeyboardInterrupt:
        pass

    # Output the results
    print("Time List:", time_list)
    print("Passenger Count List:", passenger_count_list)

    return time_list, passenger_count_list


