import streamlit as st

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
st.header("Manually Input Variables")
variable1 = st.number_input("Sonic Log", value= selected_value, key="variable1")
variable2 = st.number_input("Matrix", value=0.0, key="variable2")
variable3 = st.number_input("Fluid Flow", value=189, key="variable3")
variable4 = st.number_input("Matrix", value=0.0, key="variable4")

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
equation = f"{selected_value} - Variable 2: {variable2} / Variable 3: {variable3} - Variable 4: {variable4}"
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


