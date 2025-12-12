import streamlit as st
import leafmap.foliumap as leafmap
import pandas as pd
import geopandas as gpd
import datetime
from shapely import wkt


st.set_page_config(
    page_title="Dataset Manipulation",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


@st.cache_data
def load_climat():
    climatDF = pd.read_hdf('dataset/climat ALGERIA.h5')
    
    return climatDF

@st.cache_data
def load_soil():
    soilDF = pd.read_hdf('dataset/soil ALGERIA.h5')
    # soilDF['geometry'] = soilDF['geometry'].apply(wkt.loads)
    # soil_gdf = gpd.GeoDataFrame(soilDF, crs='epsg:4326')

    return soilDF

@st.fragment
def map_climat(df):
    col1, col2 = st.columns([3, 1])
    with col2:
        form = st.form(key="user_form")
        form.header("Search Data Point")
        search_date = form.date_input("Date", value=datetime.date(2019, 1, 1), min_value=datetime.date(2019, 1, 1), max_value=datetime.date(2019, 12, 31))
        search_time = form.time_input("Time", value=datetime.time(00, 00, 00), step=3600)
        column = form.selectbox('Column', df.columns.values.tolist()[3:])
        submit_button = form.form_submit_button('Search', type='primary')
        
    with col1:
        m = leafmap.Map(center=[28, 3.2], zoom=4)


        dt = pd.to_datetime(f"{search_date} {search_time}")
        m.add_heatmap(
            df[df['time'] == dt],
            latitude="lat",
            longitude="lon",
            value=column,
            name="Heat map",
            radius=20,
        )
        m.to_streamlit(height=700)


@st.fragment
def map_soil(df):
    col1, col2 = st.columns([3, 1])
    with col2:
        color_attribute = st.selectbox('Column', df.columns.values.tolist()[:-1])
    with col1:
        m = leafmap.Map(center=[28, 3.2], zoom=4)
        m.add_data(df.fillna(0), 
                    layer_name="Soil Data",
                    column=color_attribute,
                    fill_opacity=0.8,
                    cmap="viridis",
                    legend_title=color_attribute
                )
        m.to_streamlit(height=700)


def main():
    st.title("Data manipulation")

    file_name = st.selectbox('Select a dataset', ['climate ALGERIA', 'Soil ALGERIA'])

    if file_name == 'climate ALGERIA':
        df = load_climat()
        df = st.data_editor(df, num_rows='dynamic', use_container_width=True)

    elif file_name == 'Soil ALGERIA':
        df = load_soil()
        df = st.data_editor(df, num_rows='dynamic', use_container_width=True)
        df['geometry'] = df['geometry'].apply(wkt.loads)
        df = gpd.GeoDataFrame(df, crs='epsg:4326')
    
    
    #######################


    st.download_button(
        label="Download",
        data="",
    )


    st.title("Dataset Description")

    #######################
    # Dashboard Main Panel
    col = st.columns(3, gap='medium')

    with col[0].container(height=500, border=True):
        st.markdown('#### Dataset Information')
        
        st.metric(label="Total Rows", value=df.shape[0])
        st.metric(label="Total Columns", value=df.shape[1])
        st.metric(label="Missing Values", value=df.isnull().sum().sum())

    with col[1].container(height=500, border=True):
        st.markdown('#### Column Summary')
            # Column selection
        selected_column = st.selectbox('Select a column to analyze:', df.columns)
        selected_data_type = df[selected_column].dtype
        unique_values = df[selected_column].nunique()

        st.metric(label="Data Type", value=str(selected_data_type))
        st.metric(label="Unique Values", value=unique_values)

    with col[2].container(height=500, border=True):
        st.markdown('#### Top Values')
        top_values = df[selected_column].value_counts().head(10)
        st.dataframe(top_values,
                    column_config={
                        "states": st.column_config.TextColumn(
                            "States",
                        ),
                        "count": st.column_config.ProgressColumn(
                            "Count",
                            format="%f",
                            min_value=0,
                            max_value=max(top_values),
                        )}
                    )

    st.title("Data visualization") 

    if file_name == 'climate ALGERIA':
        map_climat(df)
    else:
        map_soil(df)
        
        


if __name__ == "__main__":
    main()