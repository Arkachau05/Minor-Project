import streamlit as st
import requests

st.set_page_config(page_title="Astrea Fairness Auditor", layout="centered")

st.title("🧠 Astrea – Dataset Fairness Auditor")

file = st.file_uploader("Upload CSV Dataset", type=["csv"])
sensitive = st.text_input("Sensitive Attribute Column (e.g. gender)")
target = st.text_input("Target Column (e.g. hired)")

if st.button("Run Fairness Audit") and file:
    with st.spinner("Analyzing dataset fairness..."):
        response = requests.post(
            "http://localhost:8000/audit-dataset/",
            files={"file": file},
            data={
                "sensitive_column": sensitive,
                "target_column": target
            }
        )

    result = response.json()

    st.subheader("📊 Fairness Summary")

    st.metric("Fairness Score", result["fairness_score"])

    st.write("**Bias Level:**", result["bias_interpretation"])

    st.subheader("📈 Group Positive Rates")
    st.bar_chart(result["positive_rate_by_group"])

    st.subheader("🧪 Fairness Metrics")
    st.json(result["fairness_metrics"])
