import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from sklearn.linear_model import LinearRegression

# -------------------
# PAGE CONFIG
# -------------------
st.set_page_config(page_title="Swiggy Dashboard", layout="wide")

st.title("🍔 Swiggy Revenue Analysis Dashboard")

# -------------------
# LOAD DATA (SAFE PATH)
# -------------------
@st.cache_data
def load_data():
    df = pd.read_excel("swiggy_data.xlsx")
    df.columns = df.columns.str.strip()
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    return df

df = load_data()

st.success("Data Loaded Successfully!")

# -------------------
# SIDEBAR FILTERS
# -------------------
st.sidebar.header("Filters")

city = st.sidebar.multiselect("Select City", df["City"].unique())
if city:
    df = df[df["City"].isin(city)]

# -------------------
# KPI METRICS
# -------------------
total_revenue = df["Price (INR)"].sum()
total_orders = len(df)
aov = total_revenue / total_orders

col1, col2, col3 = st.columns(3)

col1.metric("Total Revenue", f"₹{total_revenue:,.0f}")
col2.metric("Total Orders", total_orders)
col3.metric("Average Order Value", f"₹{aov:.2f}")

# -------------------
# DAILY REVENUE
# -------------------
st.subheader("📊 Daily Revenue Trend")

daily = df.groupby(df["Order Date"].dt.date)["Price (INR)"].sum()

fig, ax = plt.subplots()
ax.plot(daily.index, daily.values)
plt.xticks(rotation=45)

st.pyplot(fig)

# -------------------
# CITY REVENUE
# -------------------
st.subheader("🏙️ Revenue by City")

city_rev = df.groupby("City")["Price (INR)"].sum().sort_values(ascending=False)

fig = px.bar(city_rev, x=city_rev.values, y=city_rev.index, orientation="h")
st.plotly_chart(fig, use_container_width=True)

# -------------------
# FOOD CATEGORY
# -------------------
st.subheader("🍽️ Veg vs Non-Veg")

non_veg_keywords = ["chicken","egg","fish","mutton","biryani","kebab"]

df["Food Category"] = np.where(
    df["Dish Name"].str.lower().str.contains("|".join(non_veg_keywords)),
    "Non-Veg",
    "Veg"
)

food = df.groupby("Food Category")["Price (INR)"].sum().reset_index()

fig = px.pie(food, names="Food Category", values="Price (INR)", hole=0.5)
st.plotly_chart(fig)

# -------------------
# MONTHLY TREND
# -------------------
st.subheader("📈 Monthly Revenue Trend")

df["Month"] = df["Order Date"].dt.to_period("M").astype(str)
monthly = df.groupby("Month")["Price (INR)"].sum()

fig, ax = plt.subplots()
ax.bar(monthly.index, monthly.values)
plt.xticks(rotation=45)

st.pyplot(fig)

# -------------------
# SIMPLE ML PREDICTION
# -------------------
st.subheader("🤖 Revenue Prediction")

monthly_df = df.groupby(df["Order Date"].dt.to_period("M"))["Price (INR)"].sum().reset_index()
monthly_df["Month_Num"] = np.arange(len(monthly_df))

X = monthly_df[["Month_Num"]]
y = monthly_df["Price (INR)"]

model = LinearRegression()
model.fit(X, y)

future = np.arange(len(monthly_df), len(monthly_df)+4).reshape(-1,1)
pred = model.predict(future)

st.write("Next 4 Month Prediction (approx)")
st.write(pred)

st.success("Dashboard Loaded Successfully 🚀")