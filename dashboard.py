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

# Filter Data by Date Range
st.subheader("Filter Data by Date Range")
start_date, end_date = st.slider(
    "Select Date Range",
    min_value=df['week_recoded'].min().date(),
    max_value=df['week_recoded'].max().date(),
    value=(df['week_recoded'].min().date(), df['week_recoded'].max().date())
)
filtered_df = df[(df['week_recoded'] >= pd.Timestamp(start_date)) & (df['week_recoded'] <= pd.Timestamp(end_date))]
st.write(f"Filtered data from {start_date} to {end_date}")
st.dataframe(filtered_df)

# Bar Charts for Learning Modalities
st.subheader("Learning Modality Trends")
st.text("""
The bar charts below show the trends in the number of students participating in each learning modality
(Hybrid, In-Person, and Remote) over time.
""")
st.bar_chart(table, x="week", y="Hybrid", title="Hybrid Learning Trend")
st.bar_chart(table, x="week", y="In Person", title="In-Person Learning Trend")
st.bar_chart(table, x="week", y="Remote", title="Remote Learning Trend")

# Line Chart for Comparison
st.subheader("Learning Modality Comparison")
st.text("""
The line chart below provides a comparative view of the trends for all three learning modalities over time.
""")
st.line_chart(table, x="week", y=["Hybrid", "In Person", "Remote"])

# Pie Chart for Learning Modality Distribution
st.subheader("Learning Modality Distribution")
modality_data = df.groupby('learning_modality')['student_count'].sum().reset_index()
fig = px.pie(modality_data, values='student_count', names='learning_modality',
             title="Distribution of Students Across Learning Modalities")
st.plotly_chart(fig)

# Interactive Modality Selection
st.subheader("Filter by Learning Modality")
modalities = st.multiselect(
    "Select Learning Modalities to Display",
    options=df['learning_modality'].unique(),
    default=df['learning_modality'].unique()
)
filtered_modality = df[df['learning_modality'].isin(modalities)]
st.write("Filtered Data Based on Selected Modalities")
st.dataframe(filtered_modality)

# Filter Data by Minimum Student Count
st.subheader("Filter by Minimum Student Count")
min_students = st.number_input("Minimum Student Count", value=1000)
filtered_students = df[df['student_count'] >= min_students]
st.write(f"Data with student count greater than {min_students}")
st.dataframe(filtered_students)

# Footer
st.text("Dashboard created with Streamlit | Data Source: NCES")
