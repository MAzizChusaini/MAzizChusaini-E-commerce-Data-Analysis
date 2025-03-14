import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Streamlit Title
st.title("E-Commerce Dashboard")

# Load data directly
all_df = pd.read_csv("dashboard/all_data.csv")

# Ensure datetime format
all_df['order_purchase_timestamp'] = pd.to_datetime(all_df['order_purchase_timestamp'])

# Sidebar date filter
st.sidebar.write("### Filter by Date")
start_date = all_df['order_purchase_timestamp'].min().date()
end_date = all_df['order_purchase_timestamp'].max().date()

date_range = st.sidebar.date_input("Select Date Range", [start_date, end_date], min_value=start_date, max_value=end_date)

if len(date_range) == 2:
    filtered_df = all_df[(all_df['order_purchase_timestamp'].dt.date >= date_range[0]) &
                         (all_df['order_purchase_timestamp'].dt.date <= date_range[1])]
else:
    filtered_df = all_df

# KPIs
total_sales = filtered_df['payment_value'].sum()
avg_order_value = filtered_df['payment_value'].mean()
total_orders = filtered_df['order_id'].nunique()

st.write("### Key Metrics")
col1, col2, col3 = st.columns(3)
col1.metric("Total Sales", f"${total_sales:,.2f}")
col2.metric("Average Order Value", f"${avg_order_value:,.2f}")
col3.metric("Total Orders", f"{total_orders}")

col1, col2 = st.columns(2)

# Distribution of Purchase Timestamp
with col1:
    st.header("Distribusi Waktu Pembelian")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.histplot(filtered_df['order_purchase_timestamp'], kde=True, bins=30, ax=ax)
    plt.xticks(rotation=45)
    st.pyplot(fig)

# Box Plot of Product Price
with col2:
    st.header("Box Plot Harga Produk")
    fig, ax = plt.subplots(figsize=(8, 5))
    sns.boxplot(x=filtered_df['payment_value'], ax=ax)
    st.pyplot(fig)

# Heatmap Korelasi Numerik
st.header("Heatmap Korelasi Numerik")
numeric_df = filtered_df.select_dtypes(include=['number'])
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', fmt='.2f', linewidths=0.5, ax=ax)
st.pyplot(fig)

# Delivery Status (Bar and Pie)
delivery_counts = filtered_df['is_late'].value_counts()
st.header("Delivery Status")

col1, col2 = st.columns(2)

with col1:
    st.header("Late vs On-Time Deliveries")
    fig, ax = plt.subplots()
    delivery_counts.plot(kind='bar', color=['green', 'red'], ax=ax)
    plt.xticks(ticks=[0, 1], labels=['On-Time', 'Late'], rotation=0)
    ax.set_xlabel('Dev_stat')
    st.pyplot(fig)

with col2:
    st.header("Late vs On-Time Deliveries (Pie)")
    fig, ax = plt.subplots()
    custom_labels = ['On-Time', 'Late']
    delivery_counts.plot(kind='pie', autopct='%1.1f%%', colors=['green', 'red'], ax=ax, labels=custom_labels)
    ax.set_ylabel('')
    st.pyplot(fig)

# Top Products by Volume and Revenue
col1, col2 = st.columns(2)

with col1:
    st.header("5 Produk Teratas berdasarkan Volume Penjualan")
    top_volume = filtered_df.groupby('product_id')['order_item_id'].count().nlargest(5)
    st.bar_chart(top_volume)

with col2:
    st.header("5 Produk Teratas berdasarkan Revenue")
    top_revenue = filtered_df.groupby('product_id')['payment_value'].sum().nlargest(5)
    st.bar_chart(top_revenue)

st.caption('By M. Aziz Chusaini - MC211D5Y1610')
