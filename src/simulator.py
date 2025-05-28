import time, json, random
from datetime import datetime
import requests

def simulate():
    while True:
        data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "sensor_id": "wtf-pipe-1",
            "temperature": round(random.uniform(10, 35), 1),
            "pressure": round(random.uniform(1.0, 3.0), 2),
            "flow": round(random.uniform(20, 100), 1)
        }
        try:
            requests.post("http://anomaly_detector:5001/data", json=data)
        except Exception as e:
            print("Failed to send:", e)
        time.sleep(2)

if __name__ == "__main__":
    simulate()
