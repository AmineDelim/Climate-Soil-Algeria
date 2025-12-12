import streamlit as st
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely import wkt

st.set_page_config(
    page_title="Data normalization",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    upload_file = st.file_uploader("Upload your dataset", type=['h5'])
    if upload_file:
        if upload_file.name == "climat ALGERIA.h5":
            df = pd.read_hdf('dataset/climat ALGERIA.h5')
        elif upload_file.name == "climat soil ALGERIA.h5":
            df = pd.read_hdf('dataset/climat soil ALGERIA.h5')
        else:
            df = pd.read_hdf('dataset/soil ALGERIA.h5')
            # df = gpd.GeoDataFrame(df, crs='epsg:4326')


        col1, col2 = st.columns([3, 1])
        with col1.container():
            st.dataframe(df, use_container_width=True)

        with col2.form(key='user_form'):
            st.write('### Dataset Normalization')
            normalization_column = st.selectbox(
                "Choose a column:",
                df.select_dtypes(include=[np.number]).columns
            )
            normalization_choice = st.selectbox(
                "Choose a method for normalizing values:",
                ["Min-Max", "z-score"]
            )
            normalization_submit = st.form_submit_button(label='Process Normalization')

        if normalization_submit:
            # df.dropna(inplace=True)
            if normalization_choice == 'Min-Max':
                df_column = df[normalization_column].astype('float32')
                df_column = (df_column-df_column.min()) / (df_column.max()-df_column.min())
                df[normalization_column] = df_column
            else:
                df_column = df[normalization_column].astype('float32')
                df_column = (df_column - df_column.mean()) / df_column.std()
                df[normalization_column] = df_column
                
            st.write('### Result')
            col1_, col2_ = st.columns([3, 1])
            col1_.dataframe(df, use_container_width=True)


if __name__ == "__main__":
    main()