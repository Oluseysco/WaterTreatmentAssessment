from langchain.llms import LlamaCpp
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Load a local LLM via LlamaCpp
llm = LlamaCpp(model_path="/models/mistral-7b-v0.1.Q2_K.gguf", n_ctx=512, n_batch=32, temperature=0.5, max_tokens=256)
prompt_template = PromptTemplate.from_template("Generate a readable report from these anomalies: {anomalies}")
llm_chain = LLMChain(prompt=prompt_template, llm=llm)

latest_summary = "No anomalies detected."

def generate_summary():
    from detector import anomaly_log
    if not anomaly_log:
        return latest_summary
    text = json.dumps(anomaly_log[-5:])
    global latest_summary
    latest_summary = llm_chain.run(anomalies=text)
    return latest_summary
import json
import time
import requests


def fetch_anomalies():
    try:
        response = requests.get("http://localhost:5001/anomalies")
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Error fetching anomalies: {e}")
        return []   

