import streamlit as st
import geopandas as gpd
import pandas as pd
import folium
from streamlit_folium import st_folium
from folium.features import Marker, Popup, GeoJson
from shapely.geometry import Point
from shapely import wkt
import datetime

st.set_page_config(layout="wide")

@st.cache_data
def load_data():
    soilDf = pd.read_hdf('dataset/soil ALGERIA.h5')
    soil_gdf = gpd.GeoDataFrame(soilDf, crs='epsg:4326')
    climate_df = pd.read_hdf("dataset/climat ALGERIA.h5")
    return soil_gdf, climate_df

soil_gdf, climate_df = load_data()

@st.cache_data
def load_climat_soil():
    df = pd.read_hdf('dataset/climat soil ALGERIA.h5')
    return df



def map():
    # Center map on marker if it exists, otherwise use default
    center = st.session_state.marker_coords if st.session_state.marker_coords else [32, 5]
    zoom_start= 6 if st.session_state.marker_coords else 4
    m = folium.Map(location=center, zoom_start=zoom_start)

    # Add soil polygons
    tooltip = folium.GeoJsonTooltip(
        fields=soil_gdf.columns.values.tolist()[:-1],  # Exclude the geometry column
        localize=True,
        sticky=False,
        labels=True,
        style="""background-color: #F0EFEF; border: none; border-radius: 3px; box-shadow: 3px;""",
        max_width=10000,
        max_height=10000
    )
    GeoJson(
        soil_gdf,
        tooltip=tooltip,
    ).add_to(m)

    return m


@st.fragment
def part2():
# Layout: Map on one side, data on the other
    col1, col2 = st.columns([3, 1])

    # Initialize session state for marker coordinates and center
    if 'marker_coords' not in st.session_state:
        st.session_state.marker_coords = None

    # Form for user input (as it was)
    form = col2.form(key="user_form")
    form.header("Search a point")
    search_lat = form.number_input('Latitude', min_value=-90.0, max_value=90.0, value=32.0)
    search_lon = form.number_input('Longitude', min_value=-180.0, max_value=180.0, value=5.0)
    search_date = form.date_input("Date", value=datetime.date(2019, 1, 1), min_value=datetime.date(2019, 1, 1), max_value=datetime.date(2019, 12, 31))
    search_time = form.time_input("Time", value=datetime.time(00, 00, 00), step=3600)
    submit_button = form.form_submit_button('Search', type='primary')

    if submit_button:
        st.session_state.marker_coords = (search_lat, search_lon)  # Save marker coordinates

    # Display the map in Streamlit
    with col1:
        m = map()
        # Add marker if available
        if st.session_state.marker_coords:
            Marker(
                location=st.session_state.marker_coords,
                tooltip=f"Lat: {st.session_state.marker_coords[0]} Lon: {st.session_state.marker_coords[1]}",
                icon=folium.Icon(color="red")
            ).add_to(m)
        map_data = st_folium(m, width=1000, height=485, use_container_width=True)
        
        if submit_button:
            st.subheader("Climate Data")
            dt = pd.to_datetime(f"{search_date} {search_time}")
            selected_climate_df = climate_df[(climate_df['time'] == dt) & 
                                            (climate_df['lon'] == search_lon) & 
                                            (climate_df['lat'] == search_lat)]
            if len(selected_climate_df) > 0:
                st.dataframe(selected_climate_df, use_container_width=True, hide_index=True)
            else:
                st.error(f'No climate data found at {search_lon}, {search_lat}')


            # Save the selected climate data to session state
            st.session_state.selected_climate_df = selected_climate_df
        else:
            # If no form submission, use the previously stored data from session state (if available)
            if 'selected_climate_df' in st.session_state:
                selected_climate_df = st.session_state.selected_climate_df
                st.subheader("Climate Data")
                if len(selected_climate_df) > 0:
                    st.dataframe(selected_climate_df, use_container_width=True, hide_index=True)
                else:
                    st.error(f'No climate data found at {search_lon}, {search_lat}')
            else:
                st.write("No climate data selected.")

        st.subheader("Region Soil Data")
        
        if map_data.get("last_object_clicked"):
            click_info = map_data["last_object_clicked"]
            selected_df = soil_gdf[soil_gdf.geometry.contains(Point(click_info['lng'], click_info['lat']))].drop(columns='geometry')
            st.dataframe(selected_df, use_container_width=True, hide_index=True)
        else:
            st.write("Click on a region to see details.")


def main():
    df = load_climat_soil()
    st.data_editor(df, num_rows='dynamic')
    part2()


    

if __name__ == "__main__":
    main()