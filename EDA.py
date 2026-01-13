import streamlit as st
import numpy as np
import pandas as pd
import io
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="analyze your data",page_icon="",layout="wide")

st.title("📊 ANALYZE YOUR DATA")
st.write("🔍 Upload A **CSV** or an Excel file to explore your data interactively")

uploaded_file = st.file_uploader("upload a CSV or an Excel file",type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
        st.success("file upload succesfully!")
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)
        st.success("file upload succesfully!")
    else:
        st.error("could not read excel/ csv file. please check the file format.")

    # Data Overview
    st.write("### Preview of Data")
    st.dataframe(df)
        
    st.write("### 📚 Data Overview")
    st.write(f"Numbers of Rows:{df.shape[0]}")
    st.write(f"Numbers of Columns:{df.shape[1]}")
    st.write("Numbers of Missing Values:",df.isnull().sum().sum())
    st.write("Numbers of Duplicate Records:",df.duplicated().sum())

    st.write("### 📋 Complete Summary Of Dataset")
    buffer = io.StringIO()
    df.info(buf=buffer)
    i = buffer.getvalue()
    st.text(i)

    #describe()
    st.write("### 📊 Numerical Features Summary")
    st.dataframe(df.describe(include=[float, int]))

    st.write("### 📈 Statistical Summary For Non-Numerical Features Of Dataset")
    st.dataframe(df.describe(include=['bool','object']))

    st.write("### 📑 Select The Desired Columns For Analysis")
    selected_columns = st.multiselect("Choose Columns",df.columns.tolist())

    if selected_columns:
            st.dataframe(df[selected_columns].head())
    else:
            st.info("No Columns Selected. Showing Full Dataset")
            st.dataframe(df.head())

    st.write("### 📎Data Visualization")
    st.write("Select **Columns** For Data Visualization")
    columns = df.columns.tolist()
    
    num_cols = df.select_dtypes(include=['float','int']).columns
    cat_cols = df.select_dtypes(include=['object','bool']).columns

    if len(num_cols) > 0:
        x_axis = st.selectbox("Choose X-axis column", num_cols, key="x")
        y_axis = st.selectbox("Choose Y-axis column", num_cols, key="y")
    

        # Buat grid butang
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
            fig, ax = plt.subplots(figsize=(8,6))            
            ax.plot(df[x_axis], df[y_axis])
            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)
            ax.set_title(f"Line Graph of {x_axis} vs {y_axis}")
            st.pyplot(fig)

        # Scatter Graph
        if scatter_btn:
            st.write("### Scatter Graph")
            fig, ax = plt.subplots(figsize=(8,6))
            ax.scatter(df[x_axis], df[y_axis])
            ax.set_xlabel(x_axis)
            ax.set_ylabel(y_axis)
            ax.set_title(f"Scatter Graph of {x_axis} vs {y_axis}")
            st.pyplot(fig)

        # Histogram
        if hist_btn:
            st.write("### Histogram")
            fig, ax = plt.subplots(figsize=(8,6))
            ax.hist(df[x_axis], bins=20, color="skyblue", edgecolor="black")
            ax.set_title(f"Histogram of {x_axis}")
            st.pyplot(fig)

        if box_btn:
            st.write("### Boxplot")
            fig, ax = plt.subplots(figsize=(8,6))
            ax.boxplot(df[x_axis])
            ax.set_title(f"Boxplot of {x_axis}")
            st.pyplot(fig)
    
    if len(num_cols) == 0:
        st.warning("No numerical columns available.")

else:
        st.info("Please Upload A CSV File or Excel File To Get Started")