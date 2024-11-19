import streamlit as st
import pandas as pd
import plotly.express as px

# Header and Introduction
st.header("Enhanced Streamlit Dashboard: Learning Modalities and Global Education Insights")
st.subheader("Overview")
st.text("""
This dashboard visualizes data related to school learning modalities (Hybrid, In-Person, and Remote) from 2020-2021,
along with global literacy rates. Explore trends, comparisons, and insights through interactive visualizations.
""")

# Load Data (Learning Modalities)
df = pd.read_csv("https://healthdata.gov/resource/a8v3-a3m3.csv?$limit=50000")
df['week_recoded'] = pd.to_datetime(df['week'])
df['zip_code'] = df['zip_code'].astype(str)

# Load Data (Global Literacy Rates)
literacy_data = pd.read_csv("https://raw.githubusercontent.com/owid/owid-datasets/master/datasets/Literacy%20rates%20by%20country/Literacy%20rates%20by%20country.csv")

# Metrics Section
st.subheader("Data Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Learning Modalities Columns", df.shape[1])
col2.metric("Rows (Learning Modalities)", len(df))
col3.metric("Unique Districts/Schools", df['district_name'].nunique())

col4, col5 = st.columns(2)
col4.metric("Global Literacy Columns", literacy_data.shape[1])
col5.metric("Rows (Literacy Data)", len(literacy_data))

# Display Raw Data (optional toggles)
if st.checkbox("Show Raw Learning Modalities Data", value=False):
    st.dataframe(df)

if st.checkbox("Show Raw Global Literacy Data", value=False):
    st.dataframe(literacy_data)

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

# Global Literacy Analysis
st.subheader("Global Literacy Trends")
st.text("""
The following visualizations explore global literacy rates by country over time.
""")

# Literacy Rate Trend by Country
countries = st.multiselect(
    "Select Countries to Display",
    options=literacy_data["Entity"].unique(),
    default=["India", "United States", "China"]
)
filtered_literacy = literacy_data[literacy_data["Entity"].isin(countries)]

literacy_trend = px.line(
    filtered_literacy,
    x="Year",
    y="Literacy (% age 15 and above)",
    color="Entity",
    title="Literacy Rate Trends by Country",
    labels={"Year": "Year", "Literacy (% age 15 and above)": "Literacy Rate (%)", "Entity": "Country"}
)
st.plotly_chart(literacy_trend)

# Combined Analysis Placeholder
st.subheader("Combined Analysis: Learning Modalities and Literacy")
st.text("""
You can extend this section by combining insights from both datasets
to explore relationships between learning modalities and literacy trends.
""")

# Footer
st.text("Dashboard created with Streamlit | Data Sources: NCES, OWID")
