import streamlit as st
import pandas as pd
import plotly.express as px

from utils.load_data import load_sales, load_anomalies

st.set_page_config(page_title="Anomaly Report", layout="wide")

st.title("⚠️ Sales Anomaly Report")

# ---------------- Load Data ---------------- #

sales = load_sales()
anomalies = load_anomalies()

sales["Order Date"] = pd.to_datetime(
    sales["Order Date"],
    format="mixed",
    dayfirst=True,
    errors="coerce"
)


sales = sales.dropna(subset=["Order Date"])
anomalies = anomalies.dropna(subset=["Order Date"])
# ---------------- KPI ---------------- #

col1, col2 = st.columns(2)

col1.metric(
    "Total Anomalies",
    len(anomalies)
)

col2.metric(
    "Highest Anomaly Sale",
    f"${anomalies['Sales'].max():,.2f}"
)

st.divider()

# ---------------- Daily Sales ---------------- #

daily_sales = (
    sales.groupby("Order Date")["Sales"]
    .sum()
    .reset_index()
)

fig = px.line(
    daily_sales,
    x="Order Date",
    y="Sales",
    title="Daily Sales with Detected Anomalies"
)

fig.add_scatter(
    x=anomalies["Order Date"],
    y=anomalies["Sales"],
    mode="markers",
    marker=dict(
        color="red",
        size=10
    ),
    name="Anomalies"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- Table ---------------- #

st.subheader("Detected Anomalies")

st.dataframe(
    anomalies.sort_values("Order Date"),
    use_container_width=True
)

# ---------------- Download ---------------- #

st.download_button(
    label="📥 Download Anomaly Report",
    data=anomalies.to_csv(index=False),
    file_name="anomalies.csv",
    mime="text/csv"
)

# st.write(anomalies.head(10))
# st.write(anomalies.dtypes)