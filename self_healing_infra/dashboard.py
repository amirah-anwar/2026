import requests
import pandas as pd
import streamlit as st

st.title("Self-Healing Infrastructure Dashboard")

response = requests.get(
    "http://127.0.0.1:8000/services"
)

services = response.json()

df = pd.DataFrame(services)

st.subheader("Service Health")

st.dataframe(df)

alerts_response = requests.get(
    "http://127.0.0.1:8000/alerts"
)

alerts = alerts_response.json()

st.subheader("Active Alerts")

st.write(alerts)