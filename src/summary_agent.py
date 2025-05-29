import time, requests

def generate_summary():
    while True:
        try:
            resp = requests.get("http://anomaly_detector:5001/anomalies")
            anomalies = resp.json()
            if anomalies:
                prompt = f"Summarize these anomalies: {anomalies[-5:]}"
                result = requests.post("http://local_llm:8080/completion", json={"prompt": prompt, "n_predict": 100})
                summary = result.json().get("content")
                with open("logs/summary.txt", "w") as f:
                    f.write(summary)
        except Exception as e:
            print("Summary failed:", e)
        time.sleep(20)

if __name__ == "__main__":
    generate_summary()

# This script generates a summary of anomalies detected by the anomaly detector service.
# It fetches the latest anomalies every 20 seconds and sends them to a local LLM for summarization.
# The summary is then saved to a file named "summary.txt" in the logs directory.
# This is useful for providing a concise overview of recent anomalies, which can help in monitoring and decision-making.
# The script uses the requests library to interact with the anomaly detector and LLM services.
# It runs indefinitely, making it suitable for long-term monitoring of the anomaly detection system.
# The summary generation process can be adjusted by changing the frequency of the requests or the number of anomalies included in the prompt.
# The script is designed to be run in a separate process, allowing it to operate independently of the anomaly detection and LLM services.
# The summary is generated based on the last 5 anomalies to keep it concise and relevant.


