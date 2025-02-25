# ml/anomaly_detection.py

import pandas as pd
import numpy as np
from elasticsearch import Elasticsearch
from sklearn.ensemble import IsolationForest, RandomForestClassifier
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report

def fetch_logs(es_host='localhost', es_port=9200, index_pattern='siem-logs-*', size=1000):
    # Connect to Elasticsearch
    es = Elasticsearch([f'http://{es_host}:{es_port}'])
    query = {
        "query": {
            "match_all": {}
        },
        "size": size
    }
    response = es.search(index=index_pattern, body=query)
    
    # Extract logs into a list of dictionaries
    logs = []
    for hit in response['hits']['hits']:
        source = hit['_source']
        logs.append({
            "timestamp": source.get("timestamp", ""),
            "level": source.get("level", ""),
            "message": source.get("message", "")
        })
    return logs

def preprocess_logs(logs):
    # Convert logs to a DataFrame
    df = pd.DataFrame(logs)
    
    # Feature Engineering:
    # 1. Create a numeric feature: length of the message.
    df['message_length'] = df['message'].apply(len)
    
    # 2. One-hot encode the 'level' field.
    encoder = OneHotEncoder(sparse=False, handle_unknown='ignore')
    level_encoded = encoder.fit_transform(df[['level']])
    level_df = pd.DataFrame(level_encoded, columns=encoder.get_feature_names_out(['level']))
    
    # Merge features into the DataFrame
    df = pd.concat([df, level_df], axis=1)
    
    # Prepare feature set (you can add more features as needed)
    feature_columns = ['message_length'] + list(encoder.get_feature_names_out(['level']))
    features = df[feature_columns]
    
    return df, features

def perform_anomaly_detection(features):
    # Initialize Isolation Forest for unsupervised anomaly detection.
    iso_forest = IsolationForest(contamination=0.1, random_state=42)
    # IsolationForest returns -1 for anomalies and 1 for normal instances.
    predictions = iso_forest.fit_predict(features)
    return predictions

def refine_with_random_forest(features, labels):
    # For demonstration, we assume the 'labels' are the same as the anomaly flag.
    # In a real-world scenario, you'd have human-labeled data.
    X_train, X_test, y_train, y_test = train_test_split(features, labels, test_size=0.3, random_state=42)
    rf_classifier = RandomForestClassifier(random_state=42)
    rf_classifier.fit(X_train, y_train)
    y_pred = rf_classifier.predict(X_test)
    print("\nRandom Forest Classification Report:")
    print(classification_report(y_test, y_pred))

def main():
    print("Fetching logs from Elasticsearch...")
    logs = fetch_logs()
    
    if not logs:
        print("No logs retrieved. Ensure your Elasticsearch index contains data.")
        return

    print("Preprocessing logs and extracting features...")
    df, features = preprocess_logs(logs)
    
    print("Performing anomaly detection using Isolation Forest...")
    df['anomaly_flag'] = perform_anomaly_detection(features)
    # Convert IsolationForest output: mark anomalies as 1 (for -1) and normal as 0 (for 1)
    df['anomaly'] = df['anomaly_flag'].apply(lambda x: 1 if x == -1 else 0)
    
    print("Sample results:")
    print(df[['timestamp', 'level', 'message', 'anomaly']].head())
    
    # Optional: Refinement using RandomForest
    print("\nRefining anomalies with a Random Forest Classifier (using synthetic labels)...")
    # Here we assume that our anomaly flag is our ground truth for demonstration.
    refine_with_random_forest(features, df['anomaly'])
    
if __name__ == '__main__':
    main()
