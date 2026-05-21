import pandas as pd
import requests
import streamlit as st


API_BASE_URL = "http://127.0.0.1:8000"


st.set_page_config(
    page_title="AI Infrastructure Placement Agent",
    layout="wide"
)

st.title("AI Infrastructure Planning & Placement Agent")


def fetch_data(endpoint):
    response = requests.get(f"{API_BASE_URL}{endpoint}")
    response.raise_for_status()
    return response.json()


def to_table(data):
    if isinstance(data, list):
        return pd.DataFrame(data)

    if isinstance(data, dict):
        return pd.DataFrame([data])

    return pd.DataFrame([{"value": data}])


st.header("Clusters")

clusters = fetch_data("/clusters")

st.dataframe(
    to_table(clusters),
    use_container_width=True
)


st.header("Workloads")

workloads = fetch_data("/workloads")

st.dataframe(
    to_table(workloads),
    use_container_width=True
)


st.header("Placement Recommendations")

recommendations = fetch_data("/recommendations")

for item in recommendations:
    st.subheader(item["workload"])

    recommendation = item["recommendation"]

    if recommendation is None:
        st.error("No valid cluster found")
    else:
        st.success(
            f"Place on {recommendation['cluster']} "
            f"in {recommendation['region']} "
            f"with score {recommendation['score']}"
        )

    with st.expander("Ranked valid clusters"):
        st.dataframe(
            to_table(item["ranked_valid_clusters"]),
            use_container_width=True
        )

    with st.expander("Rejected clusters"):
        st.json(item["rejected_clusters"])


st.header("Capacity Forecast")

forecast = fetch_data("/forecast")

for item in forecast:
    st.subheader(item["cluster"])

    st.dataframe(
        to_table(item["forecast"]),
        use_container_width=True
    )


st.header("Self-Healing Recommendations")

self_healing = fetch_data("/self-healing")

for item in self_healing:
    st.subheader(item["workload"])

    if item["migration_needed"]:
        st.warning(
            f"Migration needed: "
            f"{item['current_cluster']} → "
            f"{item['recommended_cluster']}"
        )
    else:
        st.success(
            f"Healthy on {item['current_cluster']}"
        )

    st.write(item["reasons"])