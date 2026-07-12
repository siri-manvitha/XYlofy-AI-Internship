import pandas as pd
import streamlit as st


@st.cache_data
def load_sales():
    df = pd.read_csv("data/sales_cleaned.csv")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df


@st.cache_data
def load_forecast():
    return pd.read_csv("data/forecast.csv")


@st.cache_data
def load_anomalies():
    return pd.read_csv("data/anomalies.csv")


@st.cache_data
def load_clusters():
    return pd.read_csv("data/clusters.csv")


@st.cache_data
def load_metrics():
    return pd.read_csv("data/model_metrics.csv")