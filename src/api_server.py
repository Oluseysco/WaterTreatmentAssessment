from fastapi import FastAPI
import json, os

app = FastAPI()

@app.get("/anomalies")
def get_anomalies():
    if os.path.exists("logs/anomalies.json"):
        with open("logs/anomalies.json") as f:
            return [json.loads(line) for line in f.readlines()]
    return []

@app.get("/summary")
def get_summary():
    if os.path.exists("logs/summary.txt"):
        return {"summary": open("logs/summary.txt").read()}
    return {"summary": "No summary yet"}

@app.get("/status")
def get_status():
    return {"status": "healthy", "components": ["sensor", "detector", "llm", "api"]}
@app.get("/")
def root():
    return {"message": "Welcome to the Anomaly Detection API. Use /anomalies, /summary, or /status endpoints."}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
@app.get("/logs")

def get_logs():
    logs = []
    if os.path.exists("logs/anomalies.json"):
        with open("logs/anomalies.json") as f:
            logs.extend([json.loads(line) for line in f.readlines()])
    if os.path.exists("logs/summary.txt"):
        with open("logs/summary.txt") as f:
            logs.append({"summary": f.read()})
    return logs
    return {"logs": logs}