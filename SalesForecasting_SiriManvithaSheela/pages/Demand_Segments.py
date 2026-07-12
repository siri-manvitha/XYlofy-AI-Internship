import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Demand Segments", layout="wide")

st.title("📦 Product Demand Segments")

# Load data
clusters = pd.read_csv("data\clusters .csv")
clusters.columns = clusters.columns.str.strip()

# ---------------- KPI ---------------- #

c1, c2 = st.columns(2)

c1.metric("Total Sub-Categories", len(clusters))
c2.metric("Number of Clusters", clusters["Cluster"].nunique())

st.divider()

# ---------------- Scatter Chart ---------------- #

fig = px.scatter(
    clusters,
    x="Total Sales",
    y="Average Order Value",
    color=clusters["Cluster"].astype(str),
    hover_data=[
        "Sub-Category",
        "Growth Rate",
        "Volatility"
    ],
    size="Volatility",
    title="Demand Clusters"
)

st.plotly_chart(fig, use_container_width=True)

# ---------------- Cluster Distribution ---------------- #

cluster_counts = (
    clusters.groupby("Cluster")
    .size()
    .reset_index(name="Count")
)

fig2 = px.bar(
    cluster_counts,
    x="Cluster",
    y="Count",
    color=cluster_counts["Cluster"].astype(str),
    text="Count",
    title="Products in Each Cluster"
)

st.plotly_chart(fig2, use_container_width=True)

# ---------------- Table ---------------- #

st.subheader("Sub-Categories by Cluster")

st.dataframe(
    clusters.sort_values("Cluster"),
    use_container_width=True
)

# ---------------- Download ---------------- #

st.download_button(
    "📥 Download Cluster Report",
    data=clusters.to_csv(index=False),
    file_name="clusters.csv",
    mime="text/csv"
)