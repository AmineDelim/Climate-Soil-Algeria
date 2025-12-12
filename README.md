# Climate-Soil Algeria

A comprehensive data mining application for analyzing and preprocessing climate and soil data from Algeria.
## Overview

This application combines near-surface meteorological variables (1979-2019) with soil data for Algeria, providing an interactive Streamlit interface for data exploration, analysis, and preprocessing. The dataset focuses on 2019 data extracted from bias-corrected global reanalysis.

## Features

### A. Data Manipulation
- **Import & Visualization**: Load and display climate-soil datasets
- **Global Description**: Comprehensive dataset statistics and summaries
- **Data Editing**: Update or delete specific instances and values
- **Data Persistence**: Save processed datasets

### B. Statistical Analysis
For each attribute, the application provides:
- **Central Tendency Measures**: Mean, median, mode with symmetry analysis
- **Dispersion Measures**: Standard deviation, variance, range with outlier detection
- **Data Quality Metrics**: Missing values count and unique values analysis
- **Visual Analytics**:
  - Box plots with outlier highlighting
  - Histograms showing data distribution
  - Scatter plots for correlation analysis

### C. Data Preprocessing

#### Data Reduction
- **Redundancy Elimination**: Horizontal and vertical data reduction

#### Data Integration
- Merge climate and soil data from multiple sources into a coherent dataset

#### Data Cleaning
- **Outlier Handling**: Multiple methods for detecting and treating outliers
- **Missing Value Treatment**: Various strategies for handling missing data

#### Data Transformation
- **Normalization Methods**:
  - Min-Max scaling
  - Z-score standardization

## Usage

Install dependencies:
```bash
pip install -r requirements.txt
```

Run the application:
```bash
streamlit run App.py
```

## Dataset Information

**Source**: Near surface meteorological variables from bias-corrected reanalysis (1979-2019)  
**Year**: 2019  
**Data Types**: 
- Climate variables (temperature, precipitation, humidity, etc.)

## Packages Used

- **Xarray**: Multi-dimensional array data handling
- **GeoPandas**: Geospatial data operations
- **Plotly**: Interactive visualizations
- **Folium**: Interactive map visualizations
- **Shapely**: Geometric operations and spatial analysis
- **Streamlit**: Interactive web application framework

## Authors

- Mohamed Amine DELIM
- Sami Ilyas NOUICER