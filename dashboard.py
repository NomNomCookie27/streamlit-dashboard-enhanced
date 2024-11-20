import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import StringIO

st.header("Enhanced Streamlit Dashboard: Learning Modalities and Global Enrollment Data")
st.subheader("Overview")
st.text("""
This dashboard visualizes data related to school learning modalities (Hybrid, In-Person, and Remote) from 2020-2021,
along with global primary school enrollment data. Explore trends, comparisons, and insights through interactive visualizations.
""")

# Loading Data (Learning Modalities)
df = pd.read_csv("https://healthdata.gov/resource/a8v3-a3m3.csv?$limit=50000")
df['week_recoded'] = pd.to_datetime(df['week'])
df['zip_code'] = df['zip_code'].astype(str)

# Loading Data (Global Enrollment)
url = "https://stats.oecd.org/sdmx-json/data/DP_LIVE/.EDU_ENRL_TOTAL.../OECD?contentType=csv&detail=code&separator=comma&csv-lang=en"
response = requests.get(url)
enrollment_data = pd.read_csv(StringIO(response.text))  # Load CSV from the response text


# Clean and convert Year and Value to correct data types
# Ensure Year is numeric and Value is numeric (float)
enrollment_data['Year'] = pd.to_numeric(enrollment_data['TIME_PERIOD'], errors='coerce')
enrollment_data['Value'] = pd.to_numeric(enrollment_data['OBS_VALUE'], errors='coerce')

# Remove rows with NaN values in 'Year' or 'Value'
enrollment_data = enrollment_data.dropna(subset=['Year', 'Value'])

# Metrics Section
st.subheader("Data Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Learning Modalities Columns", df.shape[1])
col2.metric("Rows (Learning Modalities)", len(df))
col3.metric("Unique Districts/Schools", df['district_name'].nunique())

col4, col5 = st.columns(2)
col4.metric("Global Enrollment Columns", enrollment_data.shape[1])
col5.metric("Rows (Enrollment Data)", len(enrollment_data))

# Display Raw Data (optional toggles)
if st.checkbox("Show Raw Learning Modalities Data", value=False):
    st.dataframe(df)

if st.checkbox("Show Raw Global Enrollment Data", value=False):
    st.dataframe(enrollment_data)

# Pivot Table for Visualization (Learning Modalities)
table = pd.pivot_table(df, values='student_count', index=['week'],
                       columns=['learning_modality'], aggfunc="sum").reset_index()

# Learning Modalities Bar Charts
st.subheader("Learning Modality Trends")
st.text("""
The bar charts below show the trends in the number of students participating in each learning modality
(Hybrid, In-Person, and Remote) over time.
""")

# Hybrid Bar Chart
hybrid_chart = px.bar(
    table,
    x="week",
    y="Hybrid",
    title="Hybrid Learning Trend",
    labels={"week": "Week", "Hybrid": "Number of Students"}
)
st.plotly_chart(hybrid_chart)

# In-Person Bar Chart
in_person_chart = px.bar(
    table,
    x="week",
    y="In Person",
    title="In-Person Learning Trend",
    labels={"week": "Week", "In Person": "Number of Students"}
)
st.plotly_chart(in_person_chart)

# Remote Bar Chart
remote_chart = px.bar(
    table,
    x="week",
    y="Remote",
    title="Remote Learning Trend",
    labels={"week": "Week", "Remote": "Number of Students"}
)
st.plotly_chart(remote_chart)

# Line Chart for Comparison
st.subheader("Learning Modality Comparison")
st.text("""
The line chart below provides a comparative view of the trends for all three learning modalities over time.
""")
line_chart = px.line(
    table,
    x="week",
    y=["Hybrid", "In Person", "Remote"],
    title="Comparison of Learning Modalities Over Time",
    labels={"week": "Week", "value": "Number of Students", "variable": "Learning Modality"}
)
st.plotly_chart(line_chart)

# Global Enrollment Analysis
st.subheader("Global Enrollment Trends")
st.text("""
The following visualizations explore global primary school enrollment trends by country over the years.
""")

# Getting available countries from the dataset (ISO codes)
available_countries = enrollment_data["Country"].unique()


# Enrollment Trend by Country
countries = st.multiselect(
    "Select Countries to Display (ISO Codes)",
    options=available_countries,  # Use actual country codes from the dataset
    default=["CHL", "PRT", "NZL"]  # Default values; make sure they are valid country codes
)

# Handling if no country is selected
if countries:
    filtered_enrollment = enrollment_data[enrollment_data["Country"].isin(countries)]
    enrollment_trend = px.line(
        filtered_enrollment,
        x="Year",
        y="Value",
        color="Country",
        title="Primary School Enrollment Trends by Country",
        labels={"Year": "Year", "Value": "Enrollment", "Country": "Country"}
    )
    st.plotly_chart(enrollment_trend)
else:
    st.warning("Please select at least one country to display enrollment trends.")

# Combined Analysis: Enrollment and Modalities
st.subheader("Combined Analysis: Learning Modalities and Enrollment")
st.text("""
The bar chart below combines the learning modality trends with total enrollment trends for selected countries.
""")
combined_chart = px.bar(
    filtered_enrollment,
    x="Year",
    y="Value",
    title="Combined Learning Modalities and Enrollment Trends",
    labels={"Year": "Year", "Value": "Enrollment/Modality"}
)
st.plotly_chart(combined_chart)

# Footer
st.text("Dashboard created with Streamlit | Data Sources: NCES, OECD")
