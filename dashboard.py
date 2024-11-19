import streamlit as st
import pandas as pd
import requests
import plotly.express as px

# Header and Introduction
st.title("Enhanced Streamlit Dashboard")
st.header("NCES Learning Modalities Data (2020-2021)")
st.text("""
This dashboard explores school learning modalities data and incorporates a fun feature 
to suggest random activities using the Bored API. Interactive features include date filters, 
modality selection, and activity suggestions.
""")

# Load and clean NCES dataset
df = pd.read_csv("https://healthdata.gov/resource/a8v3-a3m3.csv?$limit=50000")
df['week_recoded'] = pd.to_datetime(df['week'])
df['zip_code'] = df['zip_code'].astype(str)

# Metrics
col1, col2, col3 = st.columns(3)
col1.metric("Columns", df.shape[1])
col2.metric("Rows", len(df))
col3.metric("Number of Unique Districts/Schools", df['district_name'].nunique())

# Display the first few rows of the dataset
st.subheader("Dataset Overview")
st.dataframe(df.head())

# Pivot Table for Visualizations
table = pd.pivot_table(
    df,
    values='student_count',
    index=['week'],
    columns=['learning_modality'],
    aggfunc="sum"
).reset_index()

# Visualizations
st.subheader("Learning Modality Trends Over Time")
st.bar_chart(table, x="week", y=["Hybrid", "In Person", "Remote"])
st.line_chart(table, x="week", y=["Hybrid", "In Person", "Remote"])

st.subheader("Learning Modality Distribution")
modality_data = df.groupby('learning_modality')['student_count'].sum().reset_index()
fig = px.pie(modality_data, values='student_count', names='learning_modality', title='Learning Modalities Distribution')
st.plotly_chart(fig)

# Interactive Filters
st.subheader("Filter Data")
start_date, end_date = st.slider(
    "Select Date Range",
    min_value=df['week_recoded'].min().date(),
    max_value=df['week_recoded'].max().date(),
    value=(df['week_recoded'].min().date(), df['week_recoded'].max().date())
)

filtered_df = df[(df['week_recoded'] >= pd.Timestamp(start_date)) & (df['week_recoded'] <= pd.Timestamp(end_date))]
st.write(f"Data from {start_date} to {end_date}")
st.dataframe(filtered_df)

modalities = st.multiselect(
    "Select Learning Modalities",
    options=df['learning_modality'].unique(),
    default=df['learning_modality'].unique()
)

filtered_modality = df[df['learning_modality'].isin(modalities)]
st.write("Filtered Data Based on Selected Modalities")
st.dataframe(filtered_modality)

# API Integration: Bored API
st.subheader("Feeling Bored? Try This Activity!")
st.text("""
This section uses the Bored API to fetch random activity suggestions.
Click the button below to get a new activity idea!
""")

if st.button("Get a Random Activity"):
    bored_api_url = "https://www.boredapi.com/api/activity"
    response = requests.get(bored_api_url)

    if response.status_code == 200:
        activity_data = response.json()
        st.write(f"### Activity Suggestion: {activity_data['activity']}")
        st.write(f"**Type:** {activity_data['type'].capitalize()}")
        if 'participants' in activity_data:
            st.write(f"**Participants Required:** {activity_data['participants']}")
        if 'price' in activity_data:
            st.write(f"**Price Range:** {activity_data['price']}")
    else:
        st.error("Failed to fetch activity. Please try again.")

# Footer
st.text("Dashboard created using Streamlit and the Bored API for educational purposes.")
