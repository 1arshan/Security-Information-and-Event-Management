# ml/ml_api.py

from fastapi import FastAPI
import pandas as pd
import numpy as np
from elasticsearch import Elasticsearch
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import OneHotEncoder

app = FastAPI()

def fetch_logs(es_host='elasticsearch', es_port=9200, index_pattern='siem-logs-*', size=1000):
    es = Elasticsearch([f'http://{es_host}:{es_port}'])
    query = {"query": {"match_all": {}}, "size": size}
    response = es.search(index=index_pattern, body=query)
    
    logs = []
    for hit in response['hits']['hits']:
        source = hit['_source']
        logs.append({"timestamp": source.get("timestamp", ""), "level": source.get("level", ""), "message": source.get("message", "")})
    
    return logs

def preprocess_logs(logs):
    df = pd.DataFrame(logs)
    df['message_length'] = df['message'].apply(len)
    
    encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
    level_encoded = encoder.fit_transform(df[['level']])
    level_df = pd.DataFrame(level_encoded, columns=encoder.get_feature_names_out(['level']))
    
    df = pd.concat([df, level_df], axis=1)
    feature_columns = ['message_length'] + list(encoder.get_feature_names_out(['level']))
    features = df[feature_columns]
    
    return df, features

def detect_anomalies(features):
    iso_forest = IsolationForest(contamination=0.1, random_state=42)
    predictions = iso_forest.fit_predict(features)
    return predictions

@app.get("/detect_anomalies")
def detect():
    logs = fetch_logs()
    if not logs:
        return {"error": "No logs found"}

    df, features = preprocess_logs(logs)
    df['anomaly'] = detect_anomalies(features)
    df['anomaly'] = df['anomaly'].apply(lambda x: 1 if x == -1 else 0)
    
    return df[['timestamp', 'level', 'message', 'anomaly']].to_dict(orient="records")
