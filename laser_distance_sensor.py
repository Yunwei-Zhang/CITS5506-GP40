from PiicoDev_VL53L1X import PiicoDev_VL53L1X
from datetime import datetime
import time
import requests

dataset = []
threshold_distance = 120  # Assume 100 centimeters represent 1 meter

# Value to keep track of number of people that passed by during a period, and current number of people at the place.
count = 0
current_count = 0

distSensor = PiicoDev_VL53L1X()

# Prepare starting time of packet
packet_start_time = time.time()
packet_start_date = datetime.now()
packet_start_datestring = datetime.strftime(packet_start_date, "%d-%m-%Y %H:%M:%S")

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
    
    if packet_duration > 60:
        # Only inCount or outCount can be updated due to unidirectional behaviour of this system.
        data = {
            "id": "2",
            "inCount": str(count),
            "outCount": "0",
        }
        dataset.append(data)
        
        # Send to AWS Database
        try:
            api_url = 'http://3.25.181.212:3000/api/location/updateCount'
            response = requests.patch(api_url, json=data, timeout=5)
            status = response.status_code
            if status != 200:
                print("---------------------------------------------------------------------")
                print(f"Something went wrong: {response.json()}")
                print("---------------------------------------------------------------------")
            else:
                print("---------------------------------------------------------------------")
                print('Successfully sent.')
                print("---------------------------------------------------------------------")
        except Exception as e:
            print("---------------------------------------------------------------------")
            print(f"{e.__class__.__name__}: {e}")
            print("Retry next time")
            print("---------------------------------------------------------------------")
        else:
            # Uncomment when actually sending data
            count = 0
            packet_start_time = time.time()
    
    time.sleep(0.1)

