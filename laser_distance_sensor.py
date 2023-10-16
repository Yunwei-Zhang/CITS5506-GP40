from PiicoDev_VL53L1X import PiicoDev_VL53L1X
from datetime import datetime
import time
import requests

dataset = []

# Define the threshold distance (less than 1 meter)
threshold_distance = 120  # Assume 100 centimeters represent 1 meter

# Define the threshold for the time duration for each packet
THRESHOLD_TIME = 30
threshold_time = THRESHOLD_TIME

# Value to keep track of number of people that passed by during a period, and current number of people at the place.
count = 0
current_count = 0

distSensor = PiicoDev_VL53L1X()

# Prepare starting time of packet
packet_start_time = time.time()
packet_start_date = datetime.now()
packet_start_datestring = datetime.strftime(packet_start_date, "%d-%m-%Y %H:%M:%S")

# Variable to determine if the statistics shown on the UI should be reset, should be when the system first starts.
reset = True

while True:
    dist = distSensor.read()
    dist = dist / 10
    
    if dist < threshold_distance:
        count += 1
        current_count += 1
        print("Someone passed!")
        print(f"Current count: {current_count}, Enter: {count}")
        print(f"Sensor: {dist}")
        print("come time: " + str(packet_start_datestring) + ", leave time: " + str(packet_end_datestring))
        
        # Wait for the person to pass by
        time.sleep(0.7)

    packet_end_time = time.time()
    packet_end_date = datetime.now() #8 9 1
    packet_end_datestring = datetime.strftime(packet_end_date, "%d-%m-%Y %H:%M:%S")
    packet_duration = packet_end_time - packet_start_time
    
    if packet_duration > threshold_time and count > 0:
        # Only inCount or outCount can be updated due to unidirectional behaviour of this system.
        data = {
            "id": "2",
            "startTime": str(int(packet_start_date.timestamp() * 1000)),
            "endTime": str(int(packet_end_date.timestamp() * 1000)),
            "inCount": str(count),
            "outCount": "0",
            "reset": str(reset),
        }
        print(data)
        
        dataset.append(data)
        # If dataset exceeds a size, keep most recent data on system
        if len(dataset) > 100:
            dataset.pop(0)
        
        # Send to AWS Database
        try:
            api_url = 'http://3.27.155.65:3000/api/location/updateCount'
            print("\nSending data...")
            response = requests.patch(api_url, json=data, timeout=5)
            status = response.status_code
            if status != 200:
                print("---------------------------------------------------------------------")
                print(f"Something went wrong: {response.json()}")
                print("---------------------------------------------------------------------")
                
                # Wait for another set time duration before sending again
                threshold_time += THRESHOLD_TIME
                continue
            else:
                print("---------------------------------------------------------------------")
                print('Successfully sent.')
                print("---------------------------------------------------------------------")
        except Exception as e:
            print("---------------------------------------------------------------------")
            print(f"{e.__class__.__name__}: {e}")
            print("Retry next time")
            print("---------------------------------------------------------------------")
            
            # Wait for another set time duration before sending again
            threshold_time += THRESHOLD_TIME
        else:
            # Uncomment when actually sending data
            threshold_time = THRESHOLD_TIME
            count = 0
            packet_start_time = time.time()
            if reset:
                reset = False
    
    time.sleep(0.1)

