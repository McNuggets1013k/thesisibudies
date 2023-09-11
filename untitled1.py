import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

file_path = 'C:/Users/User/Downloads/WA1.txt'  # Specify the correct file path
data = pd.read_table(file_path, delim_whitespace=True, index_col='M__DEPTH')

data = data.replace('-999.00000', np.nan)

data = data.rename(columns={'M__DEPTH': 'DEPT'})
data['DEPT'] = data.index

tops = ('Torok', 'Pebble SH', 'Walakpa SS', 'J-Klingak', 'Barrow SS', 'Klingak SH', 'T-Sag River SS', 'Shublik', 'Basement')
tops_depths = (100, 1701, 2071, 2087, 2990, 3102, 3224, 3258, 3633)

# Use st.sidebar to add sliders to the Streamlit sidebar
top_min_depth = data['DEPT'].min()
top_max_depth = data['DEPT'].max()
bottom_min_depth = data['DEPT'].min()
bottom_max_depth = data['DEPT'].max()

top_depth = st.sidebar.slider("Select Top Depth", min_value=top_min_depth, max_value=top_max_depth)
bottom_depth = st.sidebar.slider("Select Bottom Depth", min_value=bottom_min_depth, max_value=bottom_max_depth)

fig_width = st.sidebar.slider("Figure Width", min_value=6, max_value=20, value=12)
fig_height = st.sidebar.slider("Figure Height", min_value=6, max_value=20, value=10)
# Define the triple_combo_plot function with data as a parameter
def triple_combo_plot(data, top_depth, bottom_depth):
    logs = data[(data.DEPT >= top_depth) & (data.DEPT <= bottom_depth)]
    fig, ax = plt.subplots(nrows=1, ncols=3, figsize=(12, 10), sharey=True)
    fig.suptitle("Well Composite", fontsize=22)
    fig.subplots_adjust(top=0.75, wspace=0.1)

    # Ensure top_depth and bottom_depth are distinct
    if top_depth == bottom_depth:
        bottom_depth += 1 

    # General setting for all axis
    for axes in ax:
        axes.set_ylim(top_depth, bottom_depth)
        axes.invert_yaxis()
        axes.yaxis.grid(True)
        axes.get_xaxis().set_visible(False)
        for (i, j) in zip(tops_depths, tops):
            if ((i >= top_depth) and (i <= bottom_depth)):
                axes.axhline(y=i, linewidth=0.5, color='black')
                axes.text(0.1, i, j, horizontalalignment='center', verticalalignment='center')

    ax21 = ax[0].twiny()
    ax21.grid(True)
    ax21.set_xlim(140, 40)
    ax21.spines['top'].set_position(('outward', 0))
    ax21.set_xlabel('DT[us/ft]')
    ax21.plot(logs.DT, logs.DEPT, label='DT[us/ft]', color='blue')
    ax21.set_xlabel('DT[us/ft]', color='blue')
    ax21.tick_params(axis='x', colors='blue')

st.set_option('deprecation.showPyplotGlobalUse', False)
# Use st.pyplot() to display the Matplotlib plot in the Streamlit app
st.pyplot(triple_combo_plot(data, top_depth, bottom_depth))
