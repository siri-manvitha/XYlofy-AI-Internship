import streamlit as st
import pandas as pd
import plotly.express as px
from utils.load_data import load_sales

st.set_page_config(layout="wide")

st.title("📊 Sales Overview Dashboard")

df = load_sales()

# ---------------- Sidebar ---------------- #

st.sidebar.header("Filters")

years = sorted(df["Year"].unique())

selected_year = st.sidebar.multiselect(
    "Year",
    years,
    default=years
)

selected_region = st.sidebar.multiselect(
    "Region",
    sorted(df["Region"].unique()),
    default=sorted(df["Region"].unique())
)

selected_category = st.sidebar.multiselect(
    "Category",
    sorted(df["Category"].unique()),
    default=sorted(df["Category"].unique())
)

selected_segment = st.sidebar.multiselect(
    "Segment",
    sorted(df["Segment"].unique()),
    default=sorted(df["Segment"].unique())
)

filtered = df[
    (df["Year"].isin(selected_year)) &
    (df["Region"].isin(selected_region)) &
    (df["Category"].isin(selected_category)) &
    (df["Segment"].isin(selected_segment))
]

# ---------------- KPIs ---------------- #

sales = filtered["Sales"].sum()

orders = filtered["Order ID"].nunique()

customers = filtered["Customer ID"].nunique()

avg = filtered["Sales"].mean()

c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Total Sales", f"${sales:,.0f}")
c2.metric("📦 Orders", orders)
c3.metric("👥 Customers", customers)
c4.metric("📈 Avg Sales", f"${avg:,.2f}")

st.divider()

# ---------------- Charts ---------------- #

left, right = st.columns(2)

with left:

    yearly = filtered.groupby("Year")["Sales"].sum().reset_index()

    fig = px.bar(
        yearly,
        x="Year",
        y="Sales",
        title="Sales by Year",
        text_auto=".2s"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    monthly = filtered.groupby("Month Name")["Sales"].sum().reset_index()

    order = [
        "January","February","March","April","May","June",
        "July","August","September","October","November","December"
    ]

    monthly["Month Name"] = pd.Categorical(
        monthly["Month Name"],
        categories=order,
        ordered=True
    )

    monthly = monthly.sort_values("Month Name")

    fig = px.line(
        monthly,
        x="Month Name",
        y="Sales",
        markers=True,
        title="Monthly Sales Trend"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- Region ---------------- #

left, right = st.columns(2)

with left:

    region = filtered.groupby("Region")["Sales"].sum().reset_index()

    fig = px.bar(
        region,
        x="Region",
        y="Sales",
        color="Region",
        title="Sales by Region"
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    category = filtered.groupby("Category")["Sales"].sum().reset_index()

    fig = px.pie(
        category,
        names="Category",
        values="Sales",
        title="Sales by Category"
    )

    st.plotly_chart(fig, use_container_width=True)

# ---------------- Top Products ---------------- #

st.subheader("🏆 Top 10 Products")

top = (
    filtered.groupby("Product Name")["Sales"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

st.dataframe(top)