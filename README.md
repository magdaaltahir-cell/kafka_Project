# Real-Time User Interaction Dashboard

This project implements a real-time data pipeline using Kafka, MongoDB, and Streamlit.

## Components
- Producer: generates simulated user interaction events
- Consumer: processes events and computes aggregations
- MongoDB: stores aggregated data
- Streamlit Dashboard: visualizes metrics in real-time

## Metrics
- Total events
- Average interactions per user
- Most interacted item
- Least interacted item

## How to Run
1. Start Kafka
2. Run:
   python producer.py
3. Run:
   python consumer.py
4. Run dashboard:
   streamlit run dashboard.py

## Tech Stack
- Python
- Kafka
- MongoDB
- Streamlit
