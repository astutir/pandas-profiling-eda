import streamlit as st
import pandas as pd
from ydata_profiling import ProfileReport
from streamlit_pandas_profiling import st_profile_report
from sklearn.datasets import load_iris
from palmerpenguins import load_penguins
import seaborn as sns

# Custom CSS to style the entire app
st.markdown(
    """
    <style>
    /* Overall App Style */
    body {
        background-color: #f0f2f6;
    }
    
    /* Title Styling */
    .title {
        font-size: 48px;
        color: #3498db;
        font-weight: bold;
        text-align: center;
        margin-bottom: 20px;
    }

    /* Sidebar Style */
    .sidebar .sidebar-content {
        background-color: #2c3e50;
        color: white;
    }
    
    .sidebar .sidebar-content h1 {
        color: #ecf0f1;
    }
    
    .sidebar .sidebar-content label {
        color: #ecf0f1;
    }

    /* Button Styling */
    .stButton>button {
        background-color: #3498db;
        color: white;
        border-radius: 10px;
        padding: 10px 20px;
    }

    .stButton>button:hover {
        background-color: #2980b9;
        color: white;
    }

    /* Header Style */
    h2 {
        color: #2980b9;
    }

    /* Footer Info Style */
    .footer {
        text-align: center;
        font-size: 16px;
        color: #7f8c8d;
        margin-top: 50px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title and headers with custom CSS class
st.markdown('<div class="title">Pandas Profiling (EDA)</div>', unsafe_allow_html=True)

# Sidebar for user input
st.sidebar.header('Select or Upload Your Dataset')

# Option to select sample datasets
dataset_choice = st.sidebar.selectbox(
    "Choose a Sample Dataset",
    ("None", "Palmer Penguins", "Iris", "Titanic")
)

# Load selected dataset
if dataset_choice == "Palmer Penguins":
    data = load_penguins()
    input_df = data.dropna()  # Drop rows with missing values
    st.success('Loaded Palmer Penguins dataset')
elif dataset_choice == "Iris":
    iris = load_iris(as_frame=True)
    input_df = pd.concat([iris.data, iris.target.rename('species')], axis=1)
    st.success('Loaded Iris dataset')
elif dataset_choice == "Titanic":
    # Load the Titanic dataset using seaborn
    titanic = sns.load_dataset('titanic')
    input_df = titanic
    st.success('Loaded Titanic dataset')

# File uploader for CSV and Excel files
uploaded_file = st.sidebar.file_uploader('Or upload your CSV or Excel file', type=['csv', 'xlsx'])

# Use uploaded file if available
if uploaded_file is not None:
    try:
        if uploaded_file.type == 'text/csv':
            input_df = pd.read_csv(uploaded_file)
            st.success('Uploaded your CSV file')
        elif uploaded_file.type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            input_df = pd.read_excel(uploaded_file, engine='openpyxl')
            st.success('Uploaded your Excel file')
    except Exception as e:
        st.error(f"Error reading uploaded file: {e}")

# Display and analyze the dataset if available
if 'input_df' in locals():
    st.markdown('---')
    
    # Displaying a summary of the DataFrame
    st.subheader('Dataset Overview')
    st.write(input_df)
    
    # Additional Summary Statistics
    st.subheader('Data Summary')
    st.write(input_df.describe())

    # Generating and displaying the profiling report
    profile = ProfileReport(input_df, title='Data Summary Report', explorative=True)
    st.subheader('Detailed Report')
    st_profile_report(profile)
else:
    st.markdown('---')
    st.warning('Please select a dataset or upload a CSV or Excel file to proceed.')

# Footer info
st.markdown('<div class="footer">This tool helps you explore your dataset using Pandas Profiling.</div>', unsafe_allow_html=True)
