# Open Source SIEM System

This project is an open-source Security Information and Event Management (SIEM) system that integrates multiple components for log collection, processing, visualization, alerting, machine learning-based anomaly detection, and monitoring. The system is built entirely on open-source tools and is designed to be modular, scalable, and secure.

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [Components](#components)
  - [Data Collection](#data-collection)
  - [Data Ingestion and Transport](#data-ingestion-and-transport)
  - [Data Processing and Normalization](#data-processing-and-normalization)
  - [Visualization and Alerting](#visualization-and-alerting)
  - [Machine Learning and Anomaly Detection](#machine-learning-and-anomaly-detection)
  - [Monitoring and Security](#monitoring-and-security)
- [Setup and Installation](#setup-and-installation)
- [Sample Input Files](#sample-input-files)
- [Dashboard](#dashboard)
- [Usage](#usage)
- [Requirements](#requirements)
- [License](#license)

## Overview

This SIEM system is designed to:
- **Collect logs** from various sources using Fluentd.
- **Transport logs** using Kafka (with Zookeeper).
- **Process and normalize logs** using Logstash.
- **Store and visualize logs** in Elasticsearch and Kibana.
- **Alert on anomalies** using ElastAlert.
- **Detect anomalies** via a machine learning module built with FastAPI.
- **Monitor the entire pipeline** using Prometheus and Grafana.
- **Ensure security and compliance** with industry best practices.

## Architecture

The SIEM pipeline consists of several interconnected layers:

1. **Data Collection:**  
   Fluentd tails log files (e.g., `/var/log/sample.log`) and forwards logs to Kafka.

2. **Data Ingestion and Transport:**  
   Kafka, managed by Zookeeper, buffers log events for downstream processing.

3. **Data Processing and Normalization:**  
   Logstash reads logs from Kafka, processes and enriches them, and indexes the data into Elasticsearch.

4. **Visualization and Alerting:**  
   Kibana provides dashboards for data visualization, while ElastAlert triggers alerts based on defined rules.

5. **Machine Learning and Anomaly Detection:**  
   A FastAPI microservice fetches logs from Elasticsearch and uses Isolation Forest (and optionally Random Forest) to detect anomalies.

6. **Monitoring and Security:**  
   Prometheus and Grafana are used for system monitoring, and security best practices (e.g., TLS, Keycloak for IAM, audit logs) are recommended.

## Project Structure

```plaintext
siem-project/
├── alerting/
│   ├── config.yaml           # ElastAlert configuration file
│   ├── rules/                
│   │   └── test_rule.yaml    # A sample ElastAlert rule
│   └── README.md             # Documentation for the Alerting layer
├── data_collection/
│   ├── fluent.conf           # Fluentd configuration for log collection & forwarding to Kafka
│   ├── Dockerfile            # (Optional) Dockerfile for Fluentd customization
│   └── README.md             # Documentation for the Data Collection layer
├── data_processing/
│   ├── logstash.conf         # Logstash configuration for processing and normalizing logs
│   └── README.md             # Documentation for the Data Processing layer
├── ml/
│   ├── ml_api.py             # FastAPI microservice for ML anomaly detection
│   ├── Dockerfile            # Dockerfile for the ML microservice
│   └── README.md             # Documentation for the ML & Anomaly Detection module
├── monitoring/
│   ├── prometheus.yml        # Prometheus configuration file
│   ├── grafana/              # Custom Grafana dashboards & provisioning (optional)
│   └── README.md             # Documentation for Monitoring and Alerts
├── docker-compose.yml        # Docker Compose file to orchestrate all services
├── requirements.txt          # Python dependencies for custom components
└── README.md                 # Overall project documentation (this file)
