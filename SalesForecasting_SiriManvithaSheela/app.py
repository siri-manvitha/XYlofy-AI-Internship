import streamlit as st

st.set_page_config(
    page_title="Sales Forecasting System",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Sales Forecasting System")

st.markdown("""
## Welcome!

This application provides:

- 📊 Sales Overview Dashboard
- 📈 Forecast Explorer
- ⚠️ Anomaly Detection
- 📦 Product Demand Segmentation

Use the **sidebar** to navigate between pages.
""")

st.info("Built using Python, Streamlit, XGBoost, Isolation Forest and KMeans.")