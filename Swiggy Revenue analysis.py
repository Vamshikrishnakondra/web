# import libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression
# Load Dataset
df = pd.read_excel(r"C:\Users\dsaby\Downloads\swiggy_data.xlsx")
# Create sample dataset (100 rows)
sample_df = df.sample(100, random_state=42)

# Save it as new file
sample_df.to_excel("sample swiggy_data.xlsx", index=False)

df.columns
df.describe
print ("No of Rows:",df.shape[0],"No of coumns:",df.shape[1])
df.isnull().sum()
# TOTAL Restaurants 
df['Restaurant Name'].nunique()
# city orders
df['City'].value_counts()
# Daily Revenue
daily_revenue = df.groupby('Order Date')['Price (INR)'].sum()
print(daily_revenue)
# Daily Revenue plot (Mon-Sun)
df["Order Date"] = pd.to_datetime(df["Order Date"])
df["DayName"] = df["Order Date"].dt.day_name()
day_order = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
daily_revenue = (
    df.groupby("DayName")["Price (INR)"]
.sum()
.reindex(day_order)            
)
plt.figure(figsize=(10,5))
bars = plt.bar(daily_revenue.index,daily_revenue.values,color='green')
plt.xlabel("Day")
plt.ylabel("Revenue (INR)")
plt.title("Daily Revenue Trend(Mon-Sun)")
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2,
             height,
             f'{height:,.0f}',
             ha="center",
             va="bottom")

plt.tight_layout()
plt.show()
plt.figure(figsize=(6,4))
sns.heatmap(df[['Price (INR)','Rating','Rating Count']].corr(), annot=True, cmap='coolwarm')
plt.title("Correlation Matrix")
plt.show()
# Weekend vs Weekday
df['Is_Weekend'] = df['DayName'].isin(['Saturday','Sunday'])
print("\nWeekend vs Weekday Revenue:")
print(df.groupby('Is_Weekend')['Price (INR)'].sum())
# Monthly Revenue 
df['Month'] = df['Order Date'].dt.month
df.groupby('Month')['Price (INR)'].sum()
monthly_revenue = (
    df.groupby('Month')['Price (INR)']
    .sum()
    .reset_index()
)

# Monthly Revenue 
df['Month'] = df['Order Date'].dt.month
df.groupby('Month')['Price (INR)'].sum()
monthly_revenue = (
    df.groupby('Month')['Price (INR)']
    .sum()
    .reset_index()
)

# Convert to Lakhs
monthly_revenue['Revenue (Lakhs)'] = monthly_revenue['Price (INR)'] / 1e5

print(monthly_revenue[['Month','Revenue (Lakhs)']])
monthly_revenue['Revenue (Lakhs)'] = monthly_revenue['Revenue (Lakhs)'].round(2)
print(monthly_revenue)
# monthly revenue plot
df["Order Date"] = pd.to_datetime(df["Order Date"])

# Extract month name
df["Month"] = df["Order Date"].dt.strftime('%b')

# Month order
month_order = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]

monthly_revenue = (
    df.groupby("Month")["Price (INR)"]
    .sum()
    .reindex(month_order)
)

plt.figure(figsize=(10,5))

bars = plt.bar(monthly_revenue.index, monthly_revenue.values, color='blue')

plt.xlabel("Month")
plt.ylabel("Revenue (INR)")
plt.title("Monthly Revenue Trend")

# Add value labels
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2,
             height,
             f'{height:,.0f}',
             ha="center",
             va="bottom")

plt.tight_layout()
plt.show()
# monthly Revenue Trend

df["Order Date"] = pd.to_datetime(df["Order Date"])
df["YearMonth"] = df["Order Date"].dt.to_period("M").dt.to_timestamp()

monthly_revenue = df.groupby("YearMonth")["Price (INR)"].sum().reset_index()

plt.figure()
plt.plot(monthly_revenue["YearMonth"], monthly_revenue["Price (INR)"], marker='o')

plt.xlabel("Month")
plt.ylabel("Revenue (INR)")
plt.title("Monthly Revenue Trend")

# Format x-axis to show month names
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%b"))

plt.tight_layout()
plt.show()
# Revenue by state
fig = px.bar(
    df.groupby("State",as_index=False)["Price (INR)"].sum()
    .sort_values("Price (INR)",ascending=False),
    x ="Price (INR)",
    y = "State",
    orientation="h",
    title="Revenue by State (INR)"
)
fig.update_layout(height=600,yaxis=dict(autorange ="reversed"))
fig.show()
# Food category 
non_veg_keywords =[
    "chicken","egg","fish","mutton","prawn","biryani","kabab","kebab","non_veg","nonveg"

]
df['Food Category'] = np.where(
    df["Dish Name"].str.lower().str.contains("|".join(non_veg_keywords),na=False),
    "Non-veg",
    "veg"
)

food_revenue=(
    df.groupby("Food Category")["Price (INR)"]
    .sum()
    .reset_index()
)


fig = px.pie(
    food_revenue,
    values="Price (INR)",
    names="Food Category",
    hole=0.5,
    title="Revenue Contribution:veg vs Non-veg",
)
fig.update_traces(
    textinfo="percent+label",
    pull =[0.05,0]
)
fig.update_layout(
    height=500,
    margin =dict(t=60,b=40,l=40,r=40)
)
fig.show()
# Category effect: Veg vs Non-Veg revenue and rating
category_analysis = df.groupby('Food Category').agg(
    Total_Revenue=('Price (INR)','sum'),
    Avg_Rating=('Rating','mean'),
    Orders=('Dish Name','count')
).reset_index()
print("\nVeg vs Non-Veg Analysis:\n", category_analysis)

# Top 5 citeis sales
top_5_cities =(
    df.groupby("City")["Price (INR)"]
    .sum()
    .nlargest(5)
    .sort_values()
    .reset_index()
)

fig =px.bar(
    top_5_cities,
    x ="Price (INR)",
    y ="City",
    orientation="h",
    title="Top 5 cities by sales (INR)",
    color_discrete_sequence= ["red"]
)
fig.show()
# Top restuarents in Revenue
top_restaurants = df.groupby("Restaurant Name")["Price (INR)"].sum().sort_values(ascending=False).head(10)
print(top_restaurants)
# unique Dishes
unique_dishes = df['Dish Name'].nunique()
print("Unique Dishes:", unique_dishes)
# Dish list
dish_list = df['Dish Name'].unique().tolist()
print(dish_list)
# Top 10 Dishes most orderd
df['Dish Name'].value_counts().head(10)
# quaterly analysis
quarterly_summary = (df.assign(
    Order_Date =pd.to_datetime(df["Order Date"]),
    Quarter =lambda x:x["Order_Date"].dt.to_period("Q").astype(str)

).groupby("Quarter",as_index =False)
.agg(
    Total_sales =("Price (INR)","sum"),
    Avg_Rating = ("Rating","mean"),
    Total_Orders=("Order_Date","count")
).sort_values("Quarter")
)
quarterly_summary["Total_Sales"] = quarterly_summary["Total_sales"].round(0)
quarterly_summary["Avg_Rating"] = quarterly_summary["Avg_Rating"].round(2)
quarterly_summary

# applying ml model
 
# Step 1: Create monthly revenue

df['Order Date'] = pd.to_datetime(df['Order Date'])

df['YearMonth'] = df['Order Date'].dt.to_period('M').dt.to_timestamp()

monthly_revenue = df.groupby('YearMonth')['Price (INR)'].sum().reset_index()

# Step 2: Apply Linear Regression


x = np.arange(len(monthly_revenue)).reshape(-1,1)
y = monthly_revenue['Price (INR)'].values   #  important fix

model = LinearRegression()
model.fit(x, y)
# model performance
monthly_revenue = df.groupby('YearMonth')['Price (INR)'].sum().reset_index()
monthly_revenue.rename(columns={'Price (INR)': 'Revenue'}, inplace=True)

monthly_revenue['Month_Num'] = np.arange(len(monthly_revenue))

X = monthly_revenue['Month_Num'].values.reshape(-1,1)
y = monthly_revenue['Revenue'].values

model = LinearRegression()
model.fit(X, y)

# Model Evaluation
from sklearn.metrics import mean_absolute_error,r2_score
y_pred = model.predict(X)

print("\nModel Performance:")
print("MAE:", mean_absolute_error(y, y_pred))
print("R2 Score:", r2_score(y, y_pred))

print("\nModel Interpretation:")
print("Lower MAE = better prediction accuracy")
print("R2 close to 1 = good model fit")
# predicting monthly Revenue

# Prepare monthly data
monthly_revenue = df.groupby('YearMonth')['Price (INR)'].sum().reset_index()

# Create numerical feature for regression
monthly_revenue['Month_Num'] = np.arange(len(monthly_revenue))
X = monthly_revenue['Month_Num'].values.reshape(-1, 1)
y = monthly_revenue['Price (INR)'].values

# Train model
model = LinearRegression()
model.fit(X, y)
# Predict next 4 months
future_months = np.arange(len(monthly_revenue), len(monthly_revenue) + 4).reshape(-1, 1)
predicted_revenue = model.predict(future_months)


# Labels for predicted months
labels = ["Sep","Oct","Nov","Dec"]

plt.figure(figsize=(8,5))

bars = plt.bar(labels, predicted_revenue, color='orange')

plt.xlabel("Future Months")
plt.ylabel("Predicted Revenue (INR)")
plt.title("Predicted Monthly Revenue")

# Add value labels
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2,
             height,
             f'{height:,.0f}',
             ha="center",
             va="bottom")

plt.tight_layout()
plt.show()



# Prepare monthly data
monthly_revenue = df.groupby('YearMonth')['Price (INR)'].sum().reset_index()

# Create X and y
monthly_revenue['Month_Num'] = np.arange(len(monthly_revenue))

X = monthly_revenue['Month_Num'].values.reshape(-1,1)
y = monthly_revenue['Price (INR)'].values

# Train model
model = LinearRegression()
model.fit(X, y)

# Future Prediction
future_months = np.arange(len(monthly_revenue), len(monthly_revenue)+4).reshape(-1,1)
predicted_revenue = model.predict(future_months)

future_dates = pd.date_range(
    monthly_revenue['YearMonth'].max() + pd.offsets.MonthBegin(),
    periods=4, freq='MS'
)

# Plot
plt.figure(figsize=(10,5))
plt.plot(monthly_revenue['YearMonth'], y, marker='o', label='Actual')
plt.plot(future_dates, predicted_revenue, linestyle='--', color='orange', label='Predicted')
plt.legend()
plt.title("Revenue Forecast")
plt.show()

# ploting annual Revenue months (Jan-Dec)


months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
actual_rev = [6825186,6269106,6573530,6594515,6793558,6514183,6650966,6791462]
pred_rev = [6717326,6737495,6757665,6777834]

# ✅ Convert to lakhs for plotting
actual_rev_lakhs = [x / 1e5 for x in actual_rev]
pred_rev_lakhs = [x / 1e5 for x in pred_rev]

plt.figure(figsize=(10,5))

# Use the converted lists
bars1 = plt.bar(months[:8], actual_rev_lakhs, color="royalblue", label='Actual Revenue')
bars2 = plt.bar(months[8:], pred_rev_lakhs, color="orange", label="Predicted Revenue")

plt.title("Annual Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue (Lakhs INR)")
plt.legend()

# Annotate bars
bars = list(bars1) + list(bars2)
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2,
             height + 0.5,          # slightly above the bar
             f'{height:,.1f}',      # 1 decimal place
             ha='center', va='bottom')

plt.tight_layout()
plt.show()

# Quick summary metrics to support objectives
total_revenue = df['Price (INR)'].sum()
total_orders = df.shape[0]
total_restaurants = df['Restaurant Name'].nunique()
total_cities = df['City'].nunique()
top_city = df.groupby('City')['Price (INR)'].sum().idxmax()
top_dish = df.groupby('Dish Name')['Price (INR)'].sum().idxmax()

print("==== Quick Business Summary ====")
print(f"Total Revenue: ₹{total_revenue:,.0f}")
print(f"Total Orders: {total_orders}")
print(f"Number of Restaurants: {total_restaurants}")
print(f"Number of Cities: {total_cities}")
print(f"Top Revenue-Generating City: {top_city}")
print(f"Top Revenue-Generating Dish: {top_dish}")
# Reporting & Insights Summary

print("===== BUSINESS REPORT SUMMARY =====\n")

# 1️⃣ Key Metrics
print("Key Metrics:")
total_revenue = df['Price (INR)'].sum()
total_orders = df.shape[0]
AOV = total_revenue / total_orders
total_restaurants = df['Restaurant Name'].nunique()
total_cities = df['City'].nunique()
top_city = df.groupby('City')['Price (INR)'].sum().idxmax()
top_dish = df.groupby('Dish Name')['Price (INR)'].sum().idxmax()

print(f"Total Revenue: ₹{total_revenue:,.0f}")
print(f"Total Orders: {total_orders}")
print(f"Average Order Value (AOV): ₹{AOV:,.2f}\n")
print(f"Number of Restaurants: {total_restaurants}")
print(f"Number of Cities: {total_cities}")
print(f"Top Revenue-Generating City: {top_city}")
print(f"Top Revenue-Generating Dish: {top_dish}")

# 2️⃣ Top 5 Restaurants
top_restaurants = df.groupby('Restaurant Name')['Price (INR)'].sum().sort_values(ascending=False).head(5)
print("Top 5 Restaurants by Revenue:")
print(top_restaurants, "\n")

# 3️⃣ Top 5 Dishes
top_dishes = df.groupby('Dish Name')['Price (INR)'].sum().sort_values(ascending=False).head(5)
print("Top 5 Dishes by Revenue:")
print(top_dishes, "\n")

# 4️⃣ City Insights
top_cities = df.groupby('City')['Price (INR)'].sum().sort_values(ascending=False).head(5)
print("Top 5 Cities by Revenue:")
print(top_cities, "\n")

# 5️⃣ Veg vs Non-Veg
food_revenue = df.groupby('Food Category')['Price (INR)'].sum()
print("Revenue Split Veg vs Non-Veg:")
print(food_revenue, "\n")

# 6️⃣ Diagnostic Insights
corr_df = df[['Price (INR)','Rating','Rating Count']].corr()
print("Correlation Matrix (Price vs Rating vs Rating Count):")
print(corr_df, "\n")

# 7️⃣ Prescriptive Recommendations
print("Prescriptive Recommendations:")

# High performing dishes
high_performance_dishes = df.groupby('Dish Name').agg(
    Revenue=('Price (INR)','sum'),
    Avg_Rating=('Rating','mean')
)
high_perf = high_performance_dishes[
    (high_performance_dishes['Revenue'] >= high_performance_dishes['Revenue'].quantile(0.75)) & 
    (high_performance_dishes['Avg_Rating'] >= 4)
].reset_index()
print("- Promote High-Performing Dishes:")
print(high_perf[['Dish Name','Revenue','Avg_Rating']], "\n")

# Low performing dishes
low_perf = high_performance_dishes[
    (high_performance_dishes['Revenue'] <= high_performance_dishes['Revenue'].quantile(0.25)) &
    (high_performance_dishes['Avg_Rating'] <= 3.5)
].reset_index()
print("- Consider Improving or Removing Low-Performing Dishes:")
print(low_perf[['Dish Name','Revenue','Avg_Rating']], "\n")

# 8️⃣ Predicted Revenue for Next 4 Months 
pred_df = pd.DataFrame({
    'Month': ['Sep','Oct','Nov','Dec'],
    'Predicted_Revenue':np.array (predicted_revenue).astype(int)
})
print("- Predicted Revenue for Next 4 Months:")
print(pred_df, "\n")

print("===== END OF BUSINESS REPORT =====")
print("\n📊 BUSINESS INSIGHTS:")

print("- Focus on top-performing cities for marketing")
print("- Promote high revenue dishes")
print("- Improve or remove low-performing dishes")
print("- Increase staffing on weekends")
print("- Expand high-demand categories")




#full Project code
# Basic Libraries
import pandas as pd
import numpy as np

# Visualization
import matplotlib.pyplot as plt
import seaborn as sns

# ML Models
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

# Time Series
from prophet import Prophet
# Load Data
df = pd.read_excel("swiggy_data.xlsx")

print("Shape:", df.shape)
df.head()
# Data Cleaning

# Convert date
df['Order Date'] = pd.to_datetime(df['Order Date'])

# Remove duplicates
df.drop_duplicates(inplace=True)

# Handle missing values
df.dropna(inplace=True)

# Clean column names
df.columns = df.columns.str.strip()

print("After Cleaning:", df.shape)
# Feature Engineering

# Time features
df['Day'] = df['Order Date'].dt.day_name()
df['Month'] = df['Order Date'].dt.month
df['Hour'] = df['Order Date'].dt.hour

# Weekend flag
df['Is_Weekend'] = df['Day'].isin(['Saturday','Sunday'])

# Food category
non_veg_keywords = ["chicken","egg","fish","mutton","biryani","kebab"]

df['Food Category'] = np.where(
    df['Dish Name'].str.lower().str.contains("|".join(non_veg_keywords)),
    'Non-Veg','Veg'
)

# Price buckets
df['Price Bucket'] = pd.cut(df['Price (INR)'],
                           bins=[0,200,500,1000],
                           labels=['Low','Medium','High'])
# KPI Metrics
total_revenue = df['Price (INR)'].sum()
total_orders = len(df)
AOV = total_revenue / total_orders

print("===== KPI =====")
print(f"Total Revenue: ₹{total_revenue:,.0f}")
print(f"Total Orders: {total_orders}")
print(f"AOV: ₹{AOV:.2f}")
# Monthly Revenue

monthly_revenue = df.groupby(df['Order Date'].dt.to_period('M'))['Price (INR)'].sum()
monthly_revenue.index = monthly_revenue.index.to_timestamp()

plt.figure(figsize=(10,5))
monthly_revenue.plot(marker='o')
plt.title("Monthly Revenue Trend")
plt.ylabel("Revenue")
plt.show()
# Revenue By City

city_rev = df.groupby('City')['Price (INR)'].sum().sort_values(ascending=False)

plt.figure(figsize=(8,5))
city_rev.head(10).plot(kind='bar')
plt.title("Top Cities by Revenue")
plt.show()
# Peak Hours
sns.countplot(x='Hour', data=df)
plt.title("Orders by Hour")
plt.show()
# Correlation
sns.heatmap(df[['Price (INR)','Rating','Rating Count']].corr(),
            annot=True, cmap='coolwarm')
plt.show()
# Business Insights
print("===== BUSINESS INSIGHTS =====")

weekend_rev = df.groupby('Is_Weekend')['Price (INR)'].sum()

print("- Weekend revenue is higher than weekdays")

top_city = df.groupby('City')['Price (INR)'].sum().idxmax()
print(f"- Top revenue city: {top_city}")

top_dish = df.groupby('Dish Name')['Price (INR)'].sum().idxmax()
print(f"- Top dish: {top_dish}")

print("- Non-veg items contribute higher revenue")
print("- High-rated dishes drive more orders")

# weekend vs weekday
weekend = df[df['Is_Weekend'] == True]['Price (INR)'].sum()
weekday = df[df['Is_Weekend'] == False]['Price (INR)'].sum()

increase = ((weekend - weekday) / weekday) * 100

print(f"Weekend revenue is {increase:.2f}% higher than weekdays")
# ML Models

monthly_df = df.groupby(df['Order Date'].dt.to_period('M'))['Price (INR)'].sum().reset_index()
monthly_df['Order Date'] = monthly_df['Order Date'].dt.to_timestamp()

monthly_df['Month_Num'] = np.arange(len(monthly_df))

X = monthly_df[['Month_Num']]
y = monthly_df['Price (INR)']
# Model 1 Linear Regression
lr = LinearRegression()
lr.fit(X, y)

lr_pred = lr.predict(X)

print("Linear Regression MAE:", mean_absolute_error(y, lr_pred))
print("R2:", r2_score(y, lr_pred))
# Model 2 Random Forest
rf = RandomForestRegressor()
rf.fit(X, y)

rf_pred = rf.predict(X)

print("Random Forest MAE:", mean_absolute_error(y, rf_pred))
print("R2:", r2_score(y, rf_pred))
# Model 3 Prophet

prophet_df = monthly_df.rename(columns={
    'Order Date':'ds',
    'Price (INR)':'y'
})

model = Prophet()
model.fit(prophet_df)

future = model.make_future_dataframe(periods=4, freq='M')
forecast = model.predict(future)

model.plot(forecast)
plt.show()
# Future Prediction
forecast[['ds','yhat']].tail(4)
print("===== RECOMMENDATIONS =====")

print("- Focus marketing on top cities")
print("- Promote high-performing dishes")
print("- Increase weekend staffing")
print("- Improve low-rated dishes")
print("- Expand non-veg menu")
print("===== FINAL SUMMARY =====")
print(f"Revenue: ₹{total_revenue:,.0f}")
print(f"Orders: {total_orders}")
print(f"AOV: ₹{AOV:.2f}")
# print("\n===== ADVANCED INSIGHTS =====\n")

# 1. Weekend vs Weekday %
weekend = df[df['Is_Weekend'] == True]['Price (INR)'].sum()
weekday = df[df['Is_Weekend'] == False]['Price (INR)'].sum()

growth = ((weekend - weekday) / weekday) * 100
print(f"Weekend revenue is {growth:.2f}% higher than weekdays")

# 2. Top 3 cities contribution
city_rev = df.groupby('City')['Price (INR)'].sum().sort_values(ascending=False)
top3 = city_rev.head(3).sum()
total = city_rev.sum()

print(f"Top 3 cities contribute {(top3/total)*100:.2f}% of total revenue")

# 3. Veg vs Non-Veg %
food_rev = df.groupby('Food Category')['Price (INR)'].sum()

veg_pct = (food_rev['Veg']/food_rev.sum())*100
nonveg_pct = (food_rev['Non-Veg']/food_rev.sum())*100

print(f"Veg: {veg_pct:.2f}% | Non-Veg: {nonveg_pct:.2f}%")

# 4. High rating impact
high_rating = df[df['Rating'] >= 4]['Price (INR)'].sum()
low_rating = df[df['Rating'] < 4]['Price (INR)'].sum()

print(f"High-rated dishes generate {high_rating/low_rating:.2f}x more revenue")

# 5. Peak hour
peak_hour = df['Hour'].value_counts().idxmax()
print(f"Peak order hour: {peak_hour}:00")
from sklearn.cluster import KMeans

cluster_data = df[['Price (INR)', 'Rating']]

kmeans = KMeans(n_clusters=3, random_state=42)
df['Cluster'] = kmeans.fit_predict(cluster_data)

plt.figure(figsize=(8,5))
sns.scatterplot(x='Price (INR)', y='Rating', hue='Cluster', data=df)
plt.title("Customer / Dish Segmentation")
plt.show()
print("\nCluster Insights:")
print("Cluster 0: Low price, low rating → Improve quality")
print("Cluster 1: High price, high rating → Premium segment")
print("Cluster 2: Medium segment → Growth opportunity")
