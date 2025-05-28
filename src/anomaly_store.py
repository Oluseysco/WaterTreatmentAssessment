from flask import Flask, request, jsonify
from datetime import datetime, timedelta
import threading, time, json, os

app = Flask(__name__)
anomalies = []
last_seen = {}
drift_window = []

LOG_FILE = "logs/anomalies.json"

def log_anomaly(anomaly):
    anomalies.append(anomaly)
    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(anomaly) + "\n")

@app.route("/data", methods=["POST"])
def receive_data():
    data = request.get_json()
    now = datetime.fromisoformat(data["timestamp"].replace("Z", ""))
    sid = data["sensor_id"]
    last_seen[sid] = now

    # Spike detection
    if data["pressure"] > 4.0 or data["flow"] > 120:
        log_anomaly({
            "type": "spike",
            "timestamp": data["timestamp"],
            "sensor_id": sid,
            "parameter": "pressure" if data["pressure"] > 4.0 else "flow",
            "value": data["pressure"] if data["pressure"] > 4.0 else data["flow"],
            "message": "Spike detected"
        })

    # Drift detection
    drift_window.append((now, data["temperature"]))
    drift_window[:] = [(t, v) for t, v in drift_window if (now - t).total_seconds() <= 20]
    if all(v > 38 for t, v in drift_window) and len(drift_window) > 7:
        log_anomaly({
            "type": "drift",
            "timestamp": data["timestamp"],
            "sensor_id": sid,
            "parameter": "temperature",
            "value": data["temperature"],
            "duration_seconds": (now - drift_window[0][0]).seconds,
            "message": f"Temperature drift detected over {(now - drift_window[0][0]).seconds} seconds."
        })
        drift_window.clear()

    return jsonify({"status": "received"})

def dropout_check():
    while True:
        now = datetime.utcnow()
        for sid, seen_time in list(last_seen.items()):
            if (now - seen_time).total_seconds() > 10:
                log_anomaly({
                    "type": "dropout",
                    "timestamp": now.isoformat() + "Z",
                    "sensor_id": sid,
                    "message": "No data received for more than 10 seconds"
                })
                last_seen[sid] = now  # Prevent repeat alerts
        time.sleep(5)

if __name__ == "__main__":
    if not os.path.exists("logs"):
        os.mkdir("logs")
    threading.Thread(target=dropout_check, daemon=True).start()
    app.run(host="0.0.0.0", port=5001)
# Ensure the log file exists
    if not os.path.exists(LOG_FILE):
        with open(LOG_FILE, "w") as f:
            f.write("[]")  # Initialize with an empty JSON array

