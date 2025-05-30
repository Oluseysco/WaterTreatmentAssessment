from fastapi import FastAPI
from detector import anomaly_log, check_dropouts
from summary_agent import latest_summary

app = FastAPI()

@app.get("/anomalies")
def get_anomalies():
    return anomaly_log[-20:]

@app.get("/summary")
def get_summary():
    return {"summary": latest_summary}

@app.get("/status")
def get_status():
    return {"sensor_stream": "active", "llm_status": "running", "anomaly_check": "running"}
@app.get("/health")
def health_check():
    return {"status": "healthy"}
@app.get("/dropouts")
def get_dropouts():
    return check_dropouts()
@app.get("/")
def root():
    return {"message": "Anomaly Detection API is running. Use /anomalies, /summary, /status, or /dropouts endpoints."}

# This FastAPI application serves as the API server for the anomaly detection system.
# It provides endpoints to retrieve anomalies, summaries, system status, and dropout alerts.
# The `/anomalies` endpoint returns the last 20 anomalies detected.
# The `/summary` endpoint provides the latest summary of anomalies.
