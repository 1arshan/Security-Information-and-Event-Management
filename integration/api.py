# integration/api.py

from fastapi import FastAPI
from elasticsearch import Elasticsearch
from ml.anomaly_detection import fetch_logs, preprocess_logs, perform_anomaly_detection

app = FastAPI(title="SIEM Integration API", description="API to interact with the SIEM pipeline", version="1.0")

# In Docker, the service name 'elasticsearch' is used as the hostname.
ES_HOST = "elasticsearch"
ES_PORT = 9200

@app.get("/")
def read_root():
    return {"message": "SIEM Integration API is running."}

@app.get("/logs")
def get_logs(size: int = 10):
    """
    Retrieve the latest logs from Elasticsearch.
    Query Parameter:
    - size: Number of log entries to fetch.
    """
    logs = fetch_logs(es_host=ES_HOST, es_port=ES_PORT, size=size)
    return {"logs": logs}

@app.get("/anomalies")
def get_anomalies(size: int = 10):
    """
    Retrieve logs and perform anomaly detection.
    Query Parameter:
    - size: Number of log entries to fetch and analyze.
    """
    logs = fetch_logs(es_host=ES_HOST, es_port=ES_PORT, size=size)
    if not logs:
        return {"message": "No logs found."}
    
    df, features = preprocess_logs(logs)
    predictions = perform_anomaly_detection(features)
    df["anomaly"] = [1 if x == -1 else 0 for x in predictions]
    
    # Return only the logs flagged as anomalies.
    anomalies = df[df["anomaly"] == 1].to_dict(orient="records")
    return {"anomalies": anomalies}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
