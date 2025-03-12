import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Streamlit Title
st.title("E-Commerce Dashboard")

# Load data directly
all_df = pd.read_csv("all_data.csv")

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

# Payment Distribution
with col1:
    st.header("Distribution of Payment Values")
    fig, ax = plt.subplots()
    sns.histplot(filtered_df['payment_value'], kde=True, ax=ax)
    st.pyplot(fig)

# Review Score Distribution
with col2:
    st.header("Review Score Distribution")
    fig, ax = plt.subplots()
    sns.countplot(x='review_score', data=filtered_df, ax=ax)
    st.pyplot(fig)
    
col1, col2 = st.columns(2)

# Top Products by Sales
with col1:
    st.header("Top 5 Products by Sales")
    top_products = filtered_df.groupby('product_id')['payment_value'].sum().nlargest(5)
    st.bar_chart(top_products)

# Add another section for Customer Locations
with col2:
    st.write("### Top Customer Cities")
    top_cities = filtered_df['customer_city'].value_counts().nlargest(10)
    st.bar_chart(top_cities)
    
st.caption('By M. Aziz Chusaini - MC211D5Y1610')