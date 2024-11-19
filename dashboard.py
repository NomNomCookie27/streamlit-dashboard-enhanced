import streamlit as st
import pandas as pd
import plotly.express as px

# Header and Introduction
st.header("Enhanced Streamlit Dashboard: Learning Modalities Data")
st.subheader("Overview")
st.text("""
This dashboard visualizes data related to school learning modalities (Hybrid, In-Person, and Remote) from 2020-2021.
It includes interactive features, additional visualizations, and descriptive explanations for each chart.
""")

# Load Data
df = pd.read_csv("https://healthdata.gov/resource/a8v3-a3m3.csv?$limit=50000")
df['week_recoded'] = pd.to_datetime(df['week'])
df['zip_code'] = df['zip_code'].astype(str)

# Metrics Section
st.subheader("Data Overview")
col1, col2, col3 = st.columns(3)
col1.metric("Columns", df.shape[1])
col2.metric("Rows", len(df))
col3.metric("Unique Districts/Schools", df['district_name'].nunique())

# Display Raw Data (optional toggle)
if st.checkbox("Show Raw Data", value=False):
    st.dataframe(df)

# Pivot Table for Visualization
table = pd.pivot_table(df, values='student_count', index=['week'],
                       columns=['learning_modality'], aggfunc="sum").reset_index()

# Bar Charts for Learning Modalities (using Plotly)
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

# Pie Chart for Learning Modality Distribution
st.subheader("Learning Modality Distribution")
modality_data = df.groupby('learning_modality')['student_count'].sum().reset_index()
fig = px.pie(modality_data, values='student_count', names='learning_modality',
             title="Distribution of Students Across Learning Modalities")
st.plotly_chart(fig)

# Footer
st.text("Dashboard created with Streamlit | Data Source: NCES")
