# Water Treatment Facility Monitoring System

## Introduction

A python system designed to simulate a real time sensor data from a water treatment facility, detect anomalies and summarize all events using LLM and FastAPI endpoints for integration and containarise  

### Table Of Contents

1. Overview
2. Features
3. Architecture
4. Setup Instructions
5. Detection Thresholds
6. LangChain Integration
7. API Documentation
8. Local Deployment
9. Observability and Security Notes

___

## Overview

The system simulates sensor data/reading from a water treatment pipe wtf-pipe-1 and able to detect anomalies like: sudden spikes, gradual drifts and data dropouts.
I used a locally hosted llm via LangChain to help generate readable summaries of all these anomalies and provide a Rest api for consumption or interactions

## Features

 a. Anomaly Detection like spike, drift and dropout
 b. REST endpoint
 c. Local LLM with LangChain
 d. Kubernetes - using docker for deployment
 e. sensor simulators - pressure, temperature, flow per seconds etc

## Architecture

 [Sensor Simulator -----> [Anomaly Detector]     -----> [Anomaly Store + Logger]
                                              |  
                                                +------> [LangChain LLM Summary Generator]
                                              |
                                                +------>[FastAPI]

## Setup Instruction

1. How to clone the repository:  git clone https://github.comOluseysco/WaterTreatmentAssessment-Siga.git

2. Run the docker compose:  - docker -compose up --build

3. Access the endpoint: http://localhost:8000  

## Detection Threshold

| Parameter   | Normal Range | Spike Threshold | Drift Threshold     | Dropout Condition       |
| ----------- | ------------ | --------------- | ------------------- | ----------------------- |
| Temperature | 10–35°C      | > 45°C          | > 38°C for >15 secs | No data for 10+ seconds |
| Pressure    | 1.0–3.0 bar  | > 4.0 bar       | N/A                 | No data for 10+ seconds |
| Flow        | 20–100 L/min | > 120 L/min     | N/A                 | No data for 10+ seconds |

## LangChain Integration

1. LangChain agent that loads the anomaly logs and also generate the contextual summaries like this" a temperature drift occurred between 10:20 - 10:22 etc"
2. a locally hosted LLM
3. no internet access - preloaded locally or mounted via volume

## API Documentation

| Endpoint                                | Method | Description                                    |
| --------------------------------------- | ------ | ---------------------------------------------- |
| `curl http://localhost:8000/anomalies'  | GET    | Returns recent anomaly events in JSON          |
| `curl http://localhost:8000/summary'    | GET    | Returns latest natural language summary        |
| `curl http://localhost:8000/status'     | GET    | Returns health status of data stream & modules |

## Local Deployment

1. To build and run the container : docker -compose up --build
2. for logs : docker -compose logs
3. for api access : http://localhost:8000
4. check the docker -compose.yml to mount the preloaded LLM weights

## Observability and Security Notes

1. System runs fully offline
2. No external network access required
3. All model paths were stored in the .env file and injected via Docker
4. The /status to monitor and verify uptime on all component
5. All anomalies and events are stored in logs/

## The Project Structure

├── data/
├── models/
├── logs/
├── src/
│   ├── simulator.py
│   ├── detector.py
│   ├── summary_agent.py
│   ├── api_server.py
│   └── utils.py
├── Dockerfile
├── docker-compose.yml
└── README.md
