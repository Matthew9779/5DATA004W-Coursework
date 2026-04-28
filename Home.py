import streamlit as st
import pandas as pd
import plotly.express as px
# Dashboard version 1.1 - accessibility update
# Set the page title and use wide layout for more space
st.set_page_config(page_title="Home", layout="wide")

# ---- LOAD & CLEAN DATA ----
# Read the World Bank Human Capital Project dataset
df = pd.read_csv("WB_HCP_WIDEF.csv")

# Filter for total only (exclude male/female breakdowns on this page)
df = df[df['SEX_LABEL'] == 'Total']

# Define the indicators we want to use across the dashboard
indicators = [
    'Human Capital Index (HCI) (scale 0-1)',
    'Life expectancy at birth (years)',
    'Under-five mortality rate',
    'Current health expenditure (% of GDP)',
    'Expected Years of School',
    'Youth unemployment rate (%)'
]

# Keep only the rows for our selected indicators
df = df[df['INDICATOR_LABEL'].isin(indicators)]

# Define year columns to extract (2000-2023)
year_cols = [str(y) for y in range(2000, 2024)]

# Melt the dataframe from wide format to long format
# This converts year columns into a single 'Year' column
# which is required for Plotly charts
df_melted = df.melt(
    id_vars=['REF_AREA_LABEL', 'INDICATOR_LABEL'],
    value_vars=year_cols,
    var_name='Year',
    value_name='Value'
)

# Convert Year column from string to integer
df_melted['Year'] = df_melted['Year'].astype(int)

# Remove rows with no data
df_melted = df_melted.dropna(subset=['Value'])

# ---- COLOUR PALETTES ----
# Define colour palettes for each type of colour blindness
palettes = {
    "Standard": "RdYlGn",
    "Deuteranopia (red-green)": "Viridis",
    "Protanopia (red-green, dark)": "Cividis",
    "Tritanopia (blue-yellow)": "Inferno",
    "Achromatopsia (greyscale)": "Greys"
}

# Indicators where a LOWER value is BETTER
# For these we reverse the colour scale so red = bad (high) and green = good (low)
reverse_indicators = [
    'Under-five mortality rate',
    'Youth unemployment rate (%)'
]

# ---- SIDEBAR CONTROLS ----
st.sidebar.title("Controls")

# Dropdown to select which indicator to display on the map
map_indicator = st.sidebar.selectbox(
    "Select Indicator for Map",
    options=indicators,
    index=0
)

# Dropdown to select colour mode for accessibility
colour_mode = st.sidebar.selectbox(
    "Colour Mode",
    options=list(palettes.keys())
)

# Get the selected palette
palette = palettes[colour_mode]

# Check if the selected indicator needs a reversed colour scale
# Adding _r to the palette name reverses it in Plotly
reverse = map_indicator in reverse_indicators
if reverse:
    palette = palette + "_r"

# ---- PAGE TITLE ----
st.title("The Human Capital Gap")
st.markdown("*Where you are born determines your future. This dashboard explores global disparities in health, education, and opportunity.*")

# ---- WORLD MAP ----
st.subheader("Global Overview")

# Filter data for the selected indicator
indicator_df = df_melted[df_melted['INDICATOR_LABEL'] == map_indicator]

# Use the most recent year that has data for this indicator
most_recent_year = indicator_df['Year'].max()
map_df = indicator_df[indicator_df['Year'] == most_recent_year]

# Create the choropleth world map
fig_map = px.choropleth(
    map_df,
    locations='REF_AREA_LABEL',
    locationmode='country names',
    color='Value',
    color_continuous_scale=palette,
    title=f'{map_indicator} by Country ({most_recent_year})',
    labels={'Value': map_indicator}
)

# Update map layout for better appearance
fig_map.update_layout(
    height=600,
    margin=dict(l=0, r=0, t=40, b=0),
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    geo=dict(
        showframe=False,
        showcoastlines=True,
        projection_type='natural earth'
    )
)

# Display the map
st.plotly_chart(fig_map, use_container_width=True)

# Show caption with the year being displayed
st.caption(f"Showing most recent available data ({most_recent_year})")