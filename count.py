import distance_sensor as ds
import time
import json

from datetime import datetime
from gpiozero import LED

# Initialize the current count to 0
current_count = 0
enter_count = 0
leave_count = 0

# Define the threshold distance (less than 1 meter)
threshold_distance = 80  # Assume 100 centimeters represent 1 meter

# Define a variable to keep track of the previous sensor identifier
state = 0

dataset = []

res = {}
packet_start_time = time.time()
packet_start_date = datetime.now()
packet_start_datestring = datetime.strftime(packet_start_date, "%d-%m-%Y %H:%M:%S")
while True:
    res["target"] = "Bus"
    # Sensor 1: Trig 4, Echo 17
    s1, d1, t1 = ds.detect(7, 11, "sensor 1")#right
    # Sensor 2: Trig 5, Echo 35
    s2, d2, t2 = ds.detect(29, 35, "sensor 2")#left

    # If state is 0, check Sensor 1 for detecting a person passing by
    if state == 0:
        if d1 <= threshold_distance:
            state = 1
    # If state is 0, check Sensor 2 for detecting a person passing by
    if state == 0:
        if d2 <= threshold_distance:
            state = 2
    # If state is 1, check Sensor 2 for detecting a person passing by
    elif state == 1:
        if d2 <= threshold_distance:
            current_count += 1
            state = 0
            enter_count += 1
            print("count++")
            #with open('data.json','w') as json_file:
            #    json.dump(res.json_file, indent = 4)
    
    # If state is 2, check Sensor 1 for detecting a person passing by
    elif state == 2:
        if d1 <= threshold_distance:
            if current_count >= 1:
                current_count -= 1
                leave_count += 1
                print("count--")
            state = 0
            #with open('data.json','w') as json_file:
            #   json.dump(res,json_file, indent = 4)

    
    packet_end_time = time.time()
    packet_end_date = datetime.now()
    packet_end_datestring = datetime.strftime(packet_end_date, "%d-%m-%Y %H:%M:%S")
    packet_duration = packet_end_time - packet_start_time
    
    # Print the current count of people
    print("status:  " + str(state))
    print(f"Current count: {current_count}, Enter: {enter_count}, Leave: {leave_count}")
    print(f"Sensor 1: {d1}, Sensor 2: {d2}")
    print("come time: " + str(packet_start_datestring) + ", leave time: " + str(packet_end_datestring))
    print(res)

    if packet_duration > 30:
        data = {
            'time_come': packet_start_datestring,
            'time_leave': packet_end_datestring,
            'people_count': current_count,
            'enter_count': enter_count,
            'leave_count': leave_count
        }
        dataset.append(data)
        res["data"] = dataset
        packet_start_time = time.time()
        #enter_count = 0
        #leave_count = 0

    # Wait for some time before taking the next measurement
    time.sleep(0.2)
