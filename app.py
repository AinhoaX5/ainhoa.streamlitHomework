
import streamlit as st
import pandas as pd
import plotly.express as px

# Set page configuration
st.set_page_config(layout="wide", page_title="Airbnb Dashboard", page_icon="🏡")

# Load data
df = pd.read_csv("airbnb.csv")  

# Clean data
df = df.dropna(subset=["host_id", "host_name", "neighbourhood", "room_type", "price", "reviews_per_month"])  # Remove rows with missing key values
df["price"] = pd.to_numeric(df["price"], errors='coerce')  # Ensure price is numeric

# Sidebar for filters
st.sidebar.header("Filters")
neighborhood = st.sidebar.multiselect("Select Neighborhoods", df["neighbourhood"].unique(), default=df["neighbourhood"].unique())
room_type = st.sidebar.multiselect("Select Room Type", df["room_type"].unique(), default=df["room_type"].unique())
price_range = st.sidebar.slider("Select Price Range", int(df["price"].min()), int(df["price"].max()), (50, 300))

# Filter data based on sidebar selections
filtered_df = df[(df["neighbourhood"].isin(neighborhood)) &
                 (df["room_type"].isin(room_type)) &
                 (df["price"].between(price_range[0], price_range[1]))]

# Tabs for organization
tab1, tab2 = st.tabs(["📊 General Statistics", "💰 Price Analysis"])

with tab1:
    st.title("📊 General Statistics")
    
    # Top Hosts
    df_host = df.groupby(["host_id", "host_name"]).size().reset_index(name="count")
    df_host_sorted = df_host.sort_values(by="count", ascending=False).head(10)
    
    st.subheader("Top Hosts in Madrid")
    st.dataframe(df_host_sorted)
    
    # Graph 1: Top Hosts
    fig1 = px.bar(df_host_sorted, x="host_name", y="count", title="Top Hosts in Madrid", color="count")
    st.plotly_chart(fig1)
    
    # Graph 2: Listing Type vs Number of Guests
    st.subheader("Room Type vs Guests")
    fig2 = px.box(df, x="room_type", y="minimum_nights", title="Room Type vs Minimum Nights", color="room_type")
    st.plotly_chart(fig2)
    
with tab2:
    st.title("💰 Price Analysis")
    
    # Graph 3: Price by Listing Type
    st.subheader("Price by Room Type")
    fig3 = px.box(filtered_df, x="room_type", y="price", title="Price Distribution by Room Type", color="room_type")
    st.plotly_chart(fig3)
    
    # Graph 4: Reviews Per Month by Neighborhood
    st.subheader("Most Reviewed Listings per Month")
    df_reviews = df.groupby("neighbourhood")["reviews_per_month"].mean().reset_index()
    fig4 = px.bar(df_reviews, x="neighbourhood", y="reviews_per_month", title="Average Reviews Per Month by Neighborhood", color="reviews_per_month")
    st.plotly_chart(fig4)

# Price Recommendation Simulator
st.sidebar.header("🏡 Price Recommendation Simulator")
user_neighborhood = st.sidebar.selectbox("Select Neighborhood", df["neighbourhood"].unique())
user_room_type = st.sidebar.selectbox("Select Room Type", df["room_type"].unique())
user_minimum_nights = st.sidebar.slider("Minimum Nights", 1, 30, 2)

recommendation_df = df[(df["neighbourhood"] == user_neighborhood) & (df["room_type"] == user_room_type)]
recommended_price = recommendation_df["price"].median()

st.sidebar.subheader(f"💰 Suggested Price: ${recommended_price:.2f}")

st.success("Dashboard ready! Upload it to Streamlit Cloud.")
