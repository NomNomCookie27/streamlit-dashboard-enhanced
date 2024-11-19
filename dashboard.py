import streamlit as st
import pandas as pd
import plotly.express as px
import requests
from io import StringIO

# Load Data (Global Enrollment)
url = "https://stats.oecd.org/sdmx-json/data/DP_LIVE/.EDU_ENRL_TOTAL.../OECD?contentType=csv&detail=code&separator=comma&csv-lang=en"
response = requests.get(url)
enrollment_data = pd.read_csv(StringIO(response.text))  # Load CSV from the response text

# Display available columns to debug the issue
st.text("Columns in Global Enrollment Data:")
st.write(enrollment_data.columns)

# Show first few rows of the data for debugging
st.text("First 5 rows of the global enrollment data:")
st.write(enrollment_data.head())

# Check the structure of the data and identify the correct column
