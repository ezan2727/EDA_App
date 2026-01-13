import streamlit as st
import numpy as np
import pandas as pd
import io
import matplotlib.pyplot as plt


st.set_page_config(page_title="Analyze Your Data", page_icon="📊", layout="wide")

st.title("📊 ANALYZE YOUR DATA")
st.write("🔍 Upload a **CSV** or an Excel file to explore your data interactively")

uploaded_file = st.file_uploader("Upload a CSV or an Excel file", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    # Read file
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully!")
    elif uploaded_file.name.endswith(('.xlsx', '.xls')):
        df = pd.read_excel(uploaded_file)
        st.success("File uploaded successfully!")
    else:
        st.error("Could not read Excel/CSV file. Please check the file format.")

    # Data Overview
    st.write("### Preview of Data")
    st.dataframe(df)

    st.write("### 📚 Data Overview")
    st.write(f"Number of Rows: {df.shape[0]}")
    st.write(f"Number of Columns: {df.shape[1]}")
    st.write(f"Number of Missing Values: {df.isnull().sum().sum()}")
    st.write(f"Number of Duplicate Records: {df.duplicated().sum()}")

    st.write("### 📋 Complete Summary of Dataset")
    buffer = io.StringIO()
    df.info(buf=buffer)
    info_str = buffer.getvalue()
    st.text(info_str)

    # describe()
    st.write("### 📊 Numerical Features Summary")
    st.dataframe(df.describe(include=['float64', 'int64']))

    st.write("### 📈 Statistical Summary for Non-Numerical Features")
    st.dataframe(df.describe(include=['bool', 'object']))

    # Column selection
    st.write("### 📑 Select Desired Columns for Analysis")
    selected_columns = st.multiselect("Choose Columns", df.columns.tolist())

    if selected_columns:
        st.dataframe(df[selected_columns].head())
    else:
        st.info("No columns selected. Showing full dataset")
        st.dataframe(df.head())

    # Visualization
    st.write("### 📎 Data Visualization")
    st.write("Select **Columns** for Data Visualization")

    num_cols = df.select_dtypes(include=['float64', 'int64']).columns
    cat_cols = df.select_dtypes(include=['object', 'bool']).columns

    if len(num_cols) > 0:
        x_axis = st.selectbox("Choose X-axis column", num_cols, key="x")
        y_axis = st.selectbox("Choose Y-axis column", num_cols, key="y")

        # Grid buttons
        col1, col2 = st.columns(2)
        col3, col4 = st.columns(2)

        with col1:
            line_btn = st.button("Line Graph")
        with col2:
            scatter_btn = st.button("Scatter Graph")
        with col3:
            hist_btn = st.button("Histogram")
        with col4:
            box_btn = st.button("Boxplot")

        # Line Graph
        if line_btn:
            st.write("### Line Graph")
            fig, ax = plt.subplots(figsize=(6,4))
            ax.plot(df[x_axis], df[y_axis])
            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)
            ax.set_title(f"Line Graph of {x_axis} vs {y_axis}")
            st.pyplot(fig)

        # Scatter Graph
        if scatter_btn:
            st.write("### Scatter Graph")
            fig, ax = plt.subplots(figsize=(6,4))
            ax.scatter(df[x_axis], df[y_axis])
            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)
            ax.set_title(f"Scatter Graph of {x_axis} vs {y_axis}")
            st.pyplot(fig)

        # Histogram
        if hist_btn:
            st.write("### Histogram")
            fig, ax = plt.subplots(figsize=(6,4))
            ax.hist(df[x_axis].dropna(), bins=20, color="skyblue", edgecolor="black")
            ax.set_title(f"Histogram of {x_axis}")
            st.pyplot(fig)

        # Boxplot
        if box_btn:
            st.write("### Boxplot")
            fig, ax = plt.subplots(figsize=(6,4))
            ax.boxplot(df[x_axis].dropna())
            ax.set_title(f"Boxplot of {x_axis}")
            st.pyplot(fig)

    else:
        st.warning("No numerical columns available.")

else:
    st.info("Please upload a CSV or Excel file to get started")
