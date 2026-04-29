# Real-Time User Interaction Dashboard
# -----------------------------------
# This dashboard reads aggregated data from MongoDB,
# which is produced by a Kafka consumer.
# It visualizes key metrics such as:
# - Total events
# - Average interactions per user
# - Most and least interacted items
# The dashboard updates in near real-time.

import streamlit as st
import pandas as pd
import time
from pymongo import MongoClient

st.set_page_config(
    page_title="User Interaction Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Real-Time User Interaction Dashboard")
st.caption("Kafka + Python + Real-Time Metrics")

# MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["kafka_db"]
collection = db["aggregation"]

data = collection.find_one(sort=[("_id", -1)])

if data is None:
    st.warning("Waiting for data from MongoDB...")
    st.stop()

# KPI Cards
c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Events", f"{data['total_events']:,}")
c2.metric("Avg per User", round(data["average_interactions_per_user"], 2))
c3.metric("Most Interacted Item", data["most_interacted_item"])
c4.metric("Least Interacted Item", data["least_interacted_item"])

st.divider()

# Charts
left, right = st.columns(2)

with left:
    st.subheader("📈 Core Metrics")
    df = pd.DataFrame({
        "Metric": ["Total Events", "Avg per User"],
        "Value": [
            data["total_events"],
            data["average_interactions_per_user"]
        ]
    })
    st.bar_chart(df.set_index("Metric"), use_container_width=True)

with right:
    st.subheader("📊 Item Comparison")
    df2 = pd.DataFrame({
        "Type": ["Most Item", "Least Item"],
        "Item ID": [
            data["most_interacted_item"],
            data["least_interacted_item"]
        ]
    })
    st.bar_chart(df2.set_index("Type"), use_container_width=True)

st.divider()

st.subheader("📄 Live Raw Data")
st.json(data)

# Alert
if data["total_events"] > 10000:
    st.error("⚠️ High activity detected!")

# Auto refresh
time.sleep(2)
st.rerun()
