# Open SIEM Project

## Overview
Open SIEM is an open-source Security Information and Event Management (SIEM) solution designed to provide scalable log ingestion, enhanced threat detection through machine learning, and proactive monitoring and visualization of security events.

## Features
- **Scalable Log Ingestion**: Utilizes Beats, Fluentd, Logstash, Apache Kafka, and Elasticsearch/OpenSearch for efficient log collection and processing.
- **Machine Learning Integration**: Implements machine learning models for advanced threat detection capabilities.
- **Microservices Architecture**: Built using a modular microservices architecture with Docker and Kubernetes for easy deployment and scalability.
- **Proactive Monitoring**: Integrates with Kibana, Grafana, and ElastAlert for real-time monitoring and alerting.

## Project Structure
- `api/`: Contains the API service with controllers, models, routes, and services.
- `collectors/`: Includes configurations for log collectors like Beats, Fluentd, and Logstash.
- `deployment/`: Contains Docker and Kubernetes deployment configurations.
- `detection/`: Holds machine learning models and detection rules.
- `monitoring/`: Includes monitoring dashboards and configurations for Grafana and Kibana.
- `scripts/`: Contains setup and utility scripts.
- `tests/`: Includes unit and integration tests for the application.

## Getting Started
1. Clone the repository:
   ```
   git clone https://github.com/yourusername/open-siem.git
   ```
2. Navigate to the project directory:
   ```
   cd open-siem
   ```
3. Follow the setup instructions in the `scripts/setup` directory to initialize the project environment.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.