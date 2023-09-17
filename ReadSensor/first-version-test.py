import time
import requests
import json

# Initialize counters
enter_count = 0
exit_count = 0
total_count = 0

# Set the API endpoint and key for the cloud database
api_endpoint = "https://your-cloud-api-endpoint.com"
api_key = "your-api-key"

# Define the bus ID and location
bus_id = "bus001"
location = "bus_interior"

# Simulate sensor data - replace this with actual sensor data retrieval
def get_sensor_data():
    # Simulate sensor data, return a dictionary indicating whether someone entered or exited
    return {"enter": True, "exit": False}

# Send data to the cloud database
def send_data_to_cloud(data):
    headers = {"Authorization": f"Bearer {api_key}"}
    response = requests.post(f"{api_endpoint}/data", json=data, headers=headers)
    if response.status_code == 200:
        print("Data sent to the cloud successfully.")
    else:
        print("Failed to send data to the cloud.")

# Main loop
while True:
    sensor_data = get_sensor_data()

    # Update counters based on sensor data
    if sensor_data["enter"]:
        enter_count += 1
        total_count += 1
        direction = "enter"
    if sensor_data["exit"]:
        exit_count += 1
        total_count -= 1
        direction = "exit"

    # Construct the data record
    data_record = {
        "bus_id": bus_id,
        "location": location,
        "enter_count": enter_count,
        "exit_count": exit_count,
        "total_count": total_count,
        "direction": direction,
        "timestamp": int(time.time())
    }

    # Send data to the cloud database
    send_data_to_cloud(data_record)

    # Sleep for a few seconds to allow the sensor to collect new data
    time.sleep(5)
