import lasio
import pandas as pd
import streamlit as st

# Read the LAS file
las_file = lasio.read(r'C:/Users/User/Downloads/WA1.las')

# Sidebar widgets for depth selection
st.sidebar.header("Depth Selection")

# Check the available column names representing depth data in the LAS file
depth_column_names = [col.lower() for col in las_file.keys()]
if 'depth' in depth_column_names:
    depth_column_name = 'M__DEPTH'  # Use 'M__DEPTH' as the depth column name if 'depth' is found
else:
    # If 'depth' is not found, use the first column as depth by default
    depth_column_name = las_file.keys()[0]


top_depth = st.sidebar.number_input("Top Depth", min_value=las_file[depth_column_name].min(), max_value=las_file[depth_column_name].max(), value=las_file[depth_column_name].min())
bottom_depth = st.sidebar.number_input("Bottom Depth", min_value=las_file[depth_column_name].min(), max_value=las_file[depth_column_name].max(), value=las_file[depth_column_name].max())

# Display LAS file keys
st.sidebar.header("LAS File Information")
st.sidebar.write("Available Curves:")
st.sidebar.write(las_file.keys())

# Filter and display LAS data based on selected depth
well_df = las_file.df()
well_df = well_df.query(f"`{depth_column_name}` >= {top_depth} and `{depth_column_name}` <= {bottom_depth}")

# Display LAS data
st.markdown('**Filtered LAS Data**')
st.text('VSH, TPOR, EPOR, and SW are in the Last Right 4 Columns')
st.write(well_df)

# Check if 'DT' is a valid curve in the LAS file
if 'DT' in las_file.keys():
    dt_matrix = 51.3
    dt_fluid_seawater = 189
    dt_fluid_oil = 238
    st.markdown('**Sonic Porosity Calculations**')
    
    # Iterate through depth and 'DT' values and calculate sonic porosity
    for index, row in well_df.iterrows():
        d = row[depth_column_name]
        v = row['DT']
        s_seawater = (v - dt_matrix) / (dt_fluid_seawater - dt_matrix)
        s_oil = (v - dt_matrix) / (dt_fluid_oil - dt_matrix)
    
        col1, col2 = st.columns(2)  # Create two columns
        with col1:
            st.markdown(f"**Depth:** {d}")
        with col2:
            st.markdown(f"**Sonic Porosity Seawater:** {s_seawater}, **Sonic Porosity Oil:** {s_oil}")

# Options for Sonic Log
options_dict = {
    "Sandstone 57": 57,
    "Limestone 47": 47,
    "Dolomite 43.5": 43.5
}

# Sidebar widget for Sonic Log selection
st.sidebar.header("Sonic Log Selection")
selected_option = st.sidebar.radio('Select Option', list(options_dict.keys()))

# Get the numeric value of the selected option
selected_value = options_dict[selected_option]

# Manually input other variables
st.sidebar.header("Manually Input Variables")
variable2 = st.sidebar.number_input("Matrix", value=0.0, key="variable2")
variable3 = st.sidebar.number_input("Fluid Flow", value=189, key="variable3")
variable4 = st.sidebar.number_input("Matrix", value=0.0, key="variable4")

# Create a dictionary to map Sonic Log values to classifications
classification_dict = {
    57: "Sandstone",
    47: "Limestone",
    43.5: "Dolomite",
    # Add more classifications and values as needed
}

# Display the inserted variables in the main content area
st.header("Inserted Variables")
st.write(f"Sonic Log: {selected_value}")
st.write(f"Variable 2: {variable2}")
st.write(f"Variable 4: {variable4}")
st.write(f"Variable 3: {variable3}")

# Display the equation using LaTeX
equation = f"Sonic Log: {selected_value} - Variable 2: {variable2} / Variable 3: {variable3} - Variable 4: {variable4}"
st.latex(equation)

# Check if the entered Sonic Log value is in the classification_dict
if selected_value in classification_dict:
    classification = classification_dict[selected_value]
    st.write(f"Sonic Log Classification: {classification}")
else:
    st.write("Sonic Log Classification: Not Classified")

# You can perform calculations or other
# Add a button to perform calculations
if st.button("Calculate"):
    # Perform your calculation here
    result = (selected_value - variable2) / (variable3 - variable4)
    st.write(f"Result of calculation: {result}")
