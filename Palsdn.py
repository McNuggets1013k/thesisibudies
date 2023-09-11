import lasio
import streamlit as st
import pandas as pd
# Provide the correct file path without extra backslashes
las_file = lasio.read(r'C:/Users/User/Downloads/15_9-19_SR_CPI.las')

st.sidebar.write("LAS File Keys:")
st.sidebar.markdown(las_file.keys())

# Sidebar widgets for depth selection
st.sidebar.header("Depth Selection")

# Assuming you have defined 'top_depth' and 'bottom_depth' earlier in your code
# well_df = well_df.query(f"`DEPTH` >= {top_depth} and `DEPTH` <= {bottom_depth}")
well_df = las_file.df()
depth_column_name = 'DEPTH'  # Replace with the correct column name for depth data

st.markdown('**Final Result, Expand to See Full Data.**')
st.text('VSH, TPOR, EPOR, and SW are in the Last Right 4 Columns')
st.write(well_df)

# Check if 'DT' is a valid curve in the LAS file
if 'DT' in las_file.keys():
    data = []
    # Print the depth and 'DT' values
    result_container = st.container()
    for d, v in zip(las_file[depth_column_name], las_file['DT']):
        dt_matrix = 51.3
        dt_fluid_seawater = 189
        dt_fluid_oil = 238
        s_seawater = (v - dt_matrix) / (dt_fluid_seawater - dt_matrix)
        s_oil = (v - dt_matrix) / (dt_fluid_oil - dt_matrix)
        
        data.append([d, v, s_seawater, s_oil])
        
        df = pd.DataFrame(data, columns =["Depth", 'DT VAlue', 'Seawater', 'Oil'])

 # Display the DataFrame as a presentable Excel-like table
st.dataframe(df) 