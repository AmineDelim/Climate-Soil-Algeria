import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Data Reduction: Elimination of Redundancies",
    page_icon="📉",
    layout="wide",
    initial_sidebar_state="expanded"
)

def main():
    # File uploader to load datasets
    upload_file = st.file_uploader("Upload your dataset", type=['h5'])
    if upload_file:
        if upload_file.name == "climat ALGERIA.h5":
            df = pd.read_hdf('dataset/climat ALGERIA.h5')
        elif upload_file.name == "climat soil ALGERIA.h5":
            df = pd.read_hdf('dataset/climat soil ALGERIA.h5')
        elif upload_file.name == "soil ALGERIA.h5":
            df = pd.read_hdf('dataset/soil ALGERIA.h5')
        else:
            df = pd.read_hdf('dataset/test_duplicates.h5')
        
        # First row: Two columns for dataset overview and redundancy options
        col1, col2 = st.columns([1, 1])
        
        with col2.form(key='redundancy_form'):
            st.write("### Data Reduction Methods")
            # Vertical Redundancy: Remove duplicate columns
            st.write("#### Vertical Redundancy (Remove Duplicate Columns)")
            remove_duplicates_columns = st.checkbox("Remove Duplicate Columns")
            
            # Horizontal Redundancy: Remove duplicate rows
            st.write("#### Horizontal Redundancy (Remove Duplicate Rows)")
            remove_duplicates_rows = st.checkbox("Remove Duplicate Rows")
            
            # Submit button to apply changes
            submit_button = st.form_submit_button(label='Apply Reductions')

            # Apply the selected data reductions
            if submit_button:
                if remove_duplicates_columns:
                    df = df.loc[:,~df.apply(lambda x: x.duplicated(),axis=1).all()].copy()
                
                if remove_duplicates_rows:
                    df = df.drop_duplicates()
                

        # Display the dataset before applying any reductions
        st.write('### Dataset')
        st.dataframe(df, use_container_width=True)

        with col1.container(border=True):
            st.write("### Dataset Overview")
            st.write(f"Number of Rows: {df.shape[0]}")
            st.write(f"Number of Columns: {df.shape[1]}")
        


if __name__ == "__main__":
    main()
