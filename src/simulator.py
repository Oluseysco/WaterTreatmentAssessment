import random, time, json
from datetime import datetime, timezone

SENSOR_ID = "wtf-pipe-1"

NORMAL_RANGES = {
    "temperature": (10, 35),
    "pressure": (1.0, 3.0),
    "flow": (20, 100)
}

def generate_reading():
    return {
        "timestamp": datetime.utcnow().replace(tzinfo=timezone.utc).isoformat(),
        "sensor_id": SENSOR_ID,
        "temperature": round(random.uniform(*NORMAL_RANGES["temperature"]), 1),
        "pressure": round(random.uniform(*NORMAL_RANGES["pressure"]), 2),
        "flow": round(random.uniform(*NORMAL_RANGES["flow"]), 1)
    }
def simulate_sensor_data():
    while True:
        reading = generate_reading()
        print(f"Generated reading: {reading}")
        with open("sensor_data.json", "a") as f:
            f.write(json.dumps(reading) + "\n")
        time.sleep(2)  # Simulate a reading every 2 seconds 
if __name__ == "__main__":
    simulate_sensor_data()  
    
# This script simulates sensor data generation for a water treatment facility.
# It generates readings for temperature, pressure, and flow within normal ranges.
