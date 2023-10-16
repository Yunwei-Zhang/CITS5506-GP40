import distance_sensor as ds
import time
import requests

from datetime import datetime

# Initialize the current count to 0
current_count = 0
enter_count = 0
leave_count = 0
detected = False

# Define the threshold distance (less than 1 meter)
threshold_distance = 120  # Assume 100 centimeters represent 1 meter

# Define the threshold for the time duration for each packet
THRESHOLD_TIME = 30
threshold_time = THRESHOLD_TIME

# Define a variable to keep track of the previous sensor identifier
state = 0
counter = 0
COUNTER_THRESH = 5

dataset = []

res = {}
packet_start_time = time.time()
packet_start_date = datetime.now()
packet_start_datestring = datetime.strftime(packet_start_date, "%d-%m-%Y %H:%M:%S")

# Variable to determine if the statistics shown on the UI should be reset, should be when the system first starts.
reset = True

while True:
    res["target"] = "Bus"
    # Sensor 1: Trig 4, Echo 17
    #s1, d1, t1 = ds.detect(7, 11, "sensor 1")#right
    # Sensor 2: Trig 5, Echo 35
    #s2, d2, t2 = ds.detect(29, 35, "sensor 2")#left
    d1, d2, t = ds.detect()

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
            detected = True
            print("count++")
        else:
            counter += 1
            #with open('data.json','w') as json_file:
            #    json.dump(res.json_file, indent = 4)

    
    # If state is 2, check Sensor 1 for detecting a person passing by
    elif state == 2:
        if d1 <= threshold_distance:
            if current_count >= 1:
                current_count -= 1
                leave_count += 1
                detected = True
                print("count--")
            state = 0
        else:
            counter += 1
            #with open('data.json','w') as json_file:
            #   json.dump(res,json_file, indent = 4)

    
    packet_end_time = time.time()
    packet_end_date = datetime.now() #8 9 1
    packet_end_datestring = datetime.strftime(packet_end_date, "%d-%m-%Y %H:%M:%S")
    packet_duration = packet_end_time - packet_start_time
    
    if detected:
        # Print the current count of people
        print("status:  " + str(state))
        print(f"Current count: {current_count}, Enter: {enter_count}, Leave: {leave_count}")
        print(f"Sensor 1: {d1}, Sensor 2: {d2}")
        print("come time: " + str(packet_start_datestring) + ", leave time: " + str(packet_end_datestring))
        #print(res)
        detected = False
    
    if counter > COUNTER_THRESH:
        state = 0
        counter = 0

    if packet_duration > threshold_time and (enter_count > 0 or leave_count > 0):
        #data = {
        #    'id': '2',
        #    'time_come': packet_start_datestring,
        #    'time_leave': packet_end_datestring,
        #    'people_count': current_count,
        #    'inCount': enter_count,
        #    'outCount': leave_count
        #}
        data = {
            "id": "2",
            "startTime": str(int(packet_start_date.timestamp() * 1000)),
            "endTime": str(int(packet_end_date.timestamp() * 1000)),
            "inCount": str(enter_count),
            "outCount": str(leave_count),
            "reset": str(reset),
        }
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
                print('----------------------------------------------------')
                print(f"Something went wrong: {response.json()}")
                print('----------------------------------------------------')
                
                # Wait for another set time duration before sending again
                threshold_time += THRESHOLD_TIME
                continue
            else:
                print('----------------------------------------------------')
                print('Successfully sent.')
                print('----------------------------------------------------')
        except Exception as e:
            print('----------------------------------------------------')
            print(f"{e.__class__.__name__}: {e}")
            print("Retry next time")
            print('----------------------------------------------------')
            
            # Wait for another set time duration before sending again
            threshold_time += THRESHOLD_TIME
        else:
            # Uncomment when actually sending data
            enter_count = 0
            leave_count = 0
            threshold_time = THRESHOLD_TIME
            packet_start_time = time.time()
            if reset:
                reset = False
        
        res["data"] = dataset
        


    # Wait for some time before taking the next measurement
    time.sleep(0.2)
