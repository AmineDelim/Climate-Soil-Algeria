import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely import wkt
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Outliers / Missing values",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.fragment
def handle_outliers(df):
    with st.form(key='outlier_handling_form'):
        # Select column for outlier handling
        outlier_column = st.selectbox(
            "Choose a column to handle outliers:",
            df.select_dtypes(include=[np.number]).columns
        )
        
        # Outlier handling options
        outlier_option = st.selectbox(
            "Choose a method for handling outliers:",
            ["None", "Delete Outliers"]
        )

        # Submit button for outliers
        outlier_submit_button = st.form_submit_button(label='Process Outliers')

    if outlier_submit_button:
        if outlier_option == "Delete Outliers":
            # Calculate Q1 and Q3 from the original data
            q1 = df[outlier_column].quantile(0.25)
            q3 = df[outlier_column].quantile(0.75)
            iqr = q3 - q1
            lower_bound = q1 - 1.5 * iqr
            upper_bound = q3 + 1.5 * iqr
            
            # Remove outliers using precomputed Q1 and Q3
            df_filtered = df[(df[outlier_column] >= lower_bound) & (df[outlier_column] <= upper_bound)]
            
            # Boxplot comparison for the selected column
            st.write(f"### Boxplot for '{outlier_column}': Before and After Outlier Removal")
            
            fig, axes = plt.subplots(1, 2, figsize=(14, 6))
            
            # Original boxplot
            sns.boxplot(y=df[outlier_column], ax=axes[0], palette='coolwarm')
            axes[0].set_title(f'{outlier_column}: Before Outlier Removal')
            
            # Processed boxplot
            sns.boxplot(y=df_filtered[outlier_column], ax=axes[1], palette='coolwarm')
            axes[1].set_title(f'{outlier_column}: After Outlier Removal')
            
            st.pyplot(fig, use_container_width=False)


def main():
    upload_file = st.file_uploader("Upload your dataset", type=['h5'])

    if upload_file:
        if upload_file.name == "climat ALGERIA.h5":
            df = pd.read_hdf('dataset/climat ALGERIA.h5')
        elif upload_file.name == "climat soil ALGERIA.h5":
            df = pd.read_hdf('dataset/climat soil ALGERIA.h5')
        elif upload_file.name == "soil ALGERIA.h5":
            df = pd.read_hdf('dataset/soil ALGERIA.h5')
            df = gpd.GeoDataFrame(df, crs='epsg:4326')
        

        col1, col2 = st.columns([3, 1])
        with col1.container():
            st.dataframe(df, use_container_width=True)

        with col2.container(height=400, border=True):
            st.markdown('### Dataset Information')
            st.metric(label="Total Rows", value=df.shape[0])
            st.metric(label="Missing Values", value=df.isnull().sum().sum())

        #***************** Missing Values handling *****************#
        #############################################################

        st.write("### Missing Values Handling")
        missing_values_form = st.form(key="user_form")
        with missing_values_form:
            missing_values_choice = st.selectbox(
                "Choose a method for handling missing values:",
                ["None", "Delete Rows", "Replace with Mean", "Replace with Median", "Replace with Mode"]
            )
            missing_values_submit = st.form_submit_button(label='Process Missing Values')

        if missing_values_submit:
            if missing_values_choice == "Delete Rows":
                df.dropna(inplace=True)
            elif missing_values_choice == "Replace with Mean":
                for col in df.select_dtypes(include=[np.number]).columns:
                    df[col].fillna(df[col].mean(), inplace=True)
            elif missing_values_choice == "Replace with Median":
                for col in df.select_dtypes(include=[np.number]).columns:
                    df[col].fillna(df[col].median(), inplace=True)
            elif missing_values_choice == "Replace with Mode":
                for col in df.columns:
                    df[col].fillna(df[col].mode()[0], inplace=True)
            st.write("### Result")
            col1_, col2_ = st.columns([3, 1])
            with col1_.container():
                st.dataframe(df, use_container_width=True)

            with col2_.container(height=400, border=True):
                st.markdown('### Dataset Information')
                st.metric(label="Total Rows", value=df.shape[0])
                st.metric(label="Missing Values", value=df.isnull().sum().sum())
        
        #***************** Missing Values handling *****************#
        #############################################################
        st.write("### Outliers Handling")
        handle_outliers(df)



if __name__ == "__main__":
    main()