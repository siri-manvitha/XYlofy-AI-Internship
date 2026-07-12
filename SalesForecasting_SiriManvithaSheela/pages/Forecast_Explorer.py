import streamlit as st
import pandas as pd
import plotly.express as px

from utils.load_data import load_forecast, load_metrics, load_sales

st.set_page_config(page_title="Forecast Explorer", layout="wide")

st.title("📈 Forecast Explorer")

sales = load_sales()
forecast = load_forecast()
metrics = load_metrics()

# Convert dates
sales["Order Date"] = pd.to_datetime(sales["Order Date"])
forecast["Date"] = pd.to_datetime(forecast["Date"], dayfirst=True)

# Sidebar
st.sidebar.header("Forecast Settings")

forecast_type = st.sidebar.selectbox(
    "Forecast Based On",
    ["Overall Sales", "Category", "Region"]
)

horizon = st.sidebar.selectbox(
    "Forecast Horizon",
    [1, 2, 3]
)

# Historical monthly sales
history = (
    sales.groupby(pd.Grouper(key="Order Date", freq="ME"))["Sales"]
    .sum()
    .reset_index()
)

history.columns = ["Date", "Sales"]

forecast_display = forecast.head(horizon)

# Historical chart
fig = px.line(
    history,
    x="Date",
    y="Sales",
    title="Historical Sales",
    markers=True
)

# Forecast line
fig.add_scatter(
    x=forecast_display["Date"],
    y=forecast_display["Forecast"],
    mode="lines+markers",
    name="Forecast"
)

st.plotly_chart(fig, use_container_width=True)

# Forecast values
st.subheader("Forecast Values")

st.dataframe(forecast_display, use_container_width=True)

# Model metrics
st.subheader("Model Performance")

c1, c2 = st.columns(2)

mae = metrics.loc[
    metrics["Metric"] == "MAE",
    "Value"
].values[0]

rmse = metrics.loc[
    metrics["Metric"] == "RMSE",
    "Value"
].values[0]

c1.metric("MAE", f"{mae:.2f}")
c2.metric("RMSE", f"{rmse:.2f}")

# Download
st.download_button(
    "📥 Download Forecast",
    forecast_display.to_csv(index=False),
    "forecast.csv",
    "text/csv"
)