import streamlit as st
import xarray as xr
import pandas as pd
import geopandas as gpd
from shapely import wkt

st.set_page_config(page_title="Merge Demo", page_icon="⛘")

st.sidebar.header("Merge Demo")


def main():
    st.title("Merge Climate and Soil")

    col1, col2 = st.columns(2)
    uploaded_climate_file = col1.file_uploader("Upload your climate file", type=["h5"])
    uploaded_soil_file = col2.file_uploader("Upload your soil file", type=["h5"])
    
    if uploaded_climate_file and uploaded_soil_file:

        st.success("Files successfully uploaded!")

        if st.button("Merge"):
            with st.spinner("Merging climate and soil ..."):
                df = merge()
                print(df.info())
            with st.spinner("Setuping dataframe ..."):  
                st.dataframe(df)


@st.cache_data(show_spinner=False)
def merge():
    # dataset = xr.open_dataset(climateFile.read())
    # dfCLIMAT = dataset.to_dataframe().drop(columns=['spatial_ref']).reset_index().dropna(subset=['PSurf', 'Qair', 'Rainf', 'Snowf', 'Tair', 'Wind'], how='all')


    dfCLIMAT = pd.read_hdf('dataset/climat ALGERIA.h5')
    # Convert to GeoDataFrame by creating Points from lat/lon
    gdfCLIMAT = gpd.GeoDataFrame(dfCLIMAT, 
                                geometry=gpd.points_from_xy(dfCLIMAT.lon, dfCLIMAT.lat),
                                crs="EPSG:4326")  # Ensure CRS is set to WGS84 (longitude/latitude)

    dfSOIL = pd.read_hdf('dataset/soil ALGERIA.h5')
    # dfSOIL['geometry'] = dfSOIL['geometry'].apply(wkt.loads)
    gdfSOIL = gpd.GeoDataFrame(dfSOIL, crs='epsg:4326')


    # Perform a spatial join to merge the two GeoDataFrames based on the geometry
    gdf_merged = gpd.sjoin(gdfCLIMAT, gdfSOIL, how="left", predicate='within').drop(columns=['index_right', 'geometry'])

    # float32_64_cols = list(gdf_merged.select_dtypes(include=['float64', 'float32']).drop(columns=['PSurf']))
    # gdf_merged[float32_64_cols] = gdf_merged[float32_64_cols].astype('float16')


    return gdf_merged.reset_index(drop=True)


if __name__ == "__main__":
    main()

