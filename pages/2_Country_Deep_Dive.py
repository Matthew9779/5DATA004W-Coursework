import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
# Added country comparison feature - dual line charts with dashed comparison line
# Set page title and wide layout
st.set_page_config(page_title="Country Deep Dive", layout="wide")

# ---- LOAD & CLEAN DATA ----
# Read the World Bank Human Capital Project dataset
df = pd.read_csv("WB_HCP_WIDEF.csv")

# Filter for total only (exclude male/female breakdowns)
df = df[df['SEX_LABEL'] == 'Total']

# Define the indicators we need for this page
indicators = [
    'Human Capital Index (HCI) (scale 0-1)',
    'Life expectancy at birth (years)',
    'Under-five mortality rate',
    'Youth unemployment rate (%)'
]

# Keep only rows for our selected indicators
df = df[df['INDICATOR_LABEL'].isin(indicators)]

# Define year columns to extract (2000-2023)
year_cols = [str(y) for y in range(2000, 2024)]

# Melt from wide to long format for Plotly compatibility
df_melted = df.melt(
    id_vars=['REF_AREA_LABEL', 'INDICATOR_LABEL'],
    value_vars=year_cols,
    var_name='Year',
    value_name='Value'
)

# Convert Year to integer and drop missing values
df_melted['Year'] = df_melted['Year'].astype(int)
df_melted = df_melted.dropna(subset=['Value'])

# ---- COLOUR PALETTES ----
# Define line colours for each type of colour blindness
# First colour = primary country, second colour = comparison country
colour_sequences = {
    "Standard": ['#636EFA', '#EF553B'],
    "Deuteranopia (red-green)": ['#E69F00', '#56B4E9'],
    "Protanopia (red-green, dark)": ['#88CCEE', '#DDCC77'],
    "Tritanopia (blue-yellow)": ['#CC6677', '#44AA99'],
    "Achromatopsia (greyscale)": ['#FFFFFF', '#808080']
}

# ---- SIDEBAR CONTROLS ----
st.sidebar.title("Controls")

# Get sorted list of all countries in the dataset
countries = sorted(df_melted['REF_AREA_LABEL'].unique().tolist())

# Primary country dropdown
selected_country = st.sidebar.selectbox(
    "Select Country",
    options=countries,
    index=countries.index('United Kingdom')
)

# Comparison country dropdown (optional)
compare_options = ['None'] + countries
selected_compare = st.sidebar.selectbox(
    "Compare With",
    options=compare_options,
    index=0
)

# Colour mode dropdown for accessibility
colour_mode = st.sidebar.selectbox(
    "Colour Mode",
    options=list(colour_sequences.keys())
)

# Get the selected colour pair
colours = colour_sequences[colour_mode]
primary_colour = colours[0]
compare_colour = colours[1]

# ---- PAGE TITLE ----
st.title("Country Deep Dive")

# Update subtitle based on whether comparison is selected
if selected_compare != 'None':
    st.markdown(f"*Comparing **{selected_country}** and **{selected_compare}** over time.*")
else:
    st.markdown(f"*Exploring human capital trends for **{selected_country}** over time.*")

# ---- HELPER FUNCTION ----
def make_line_chart(indicator, title, primary_country, compare_country, primary_col, compare_col):
    """
    Creates a line chart for a given indicator.
    Shows primary country always, and comparison country if selected.
    """
    # Filter data for primary country
    primary_df = df_melted[
        (df_melted['REF_AREA_LABEL'] == primary_country) &
        (df_melted['INDICATOR_LABEL'] == indicator)
    ].sort_values('Year')

    # Create figure
    fig = go.Figure()

    # Add primary country line
    fig.add_trace(go.Scatter(
        x=primary_df['Year'],
        y=primary_df['Value'],
        mode='lines',
        name=primary_country,
        line=dict(color=primary_col, width=2)
    ))

    # Add comparison country line if selected
    if compare_country != 'None':
        compare_df = df_melted[
            (df_melted['REF_AREA_LABEL'] == compare_country) &
            (df_melted['INDICATOR_LABEL'] == indicator)
        ].sort_values('Year')

        fig.add_trace(go.Scatter(
            x=compare_df['Year'],
            y=compare_df['Value'],
            mode='lines',
            name=compare_country,
            line=dict(color=compare_col, width=2, dash='dash')
        ))

    # Update layout for dark theme
    fig.update_layout(
        title=title,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font_color='white',
        legend=dict(bgcolor='rgba(0,0,0,0)'),
        height=300,
        margin=dict(t=40, b=40, l=40, r=40)
    )

    return fig

# ---- CHARTS ----
# Display charts in a 2x2 grid
col1, col2 = st.columns(2)
col3, col4 = st.columns(2)

# Human Capital Index chart
with col1:
    fig = make_line_chart(
        'Human Capital Index (HCI) (scale 0-1)',
        'Human Capital Index',
        selected_country,
        selected_compare,
        primary_colour,
        compare_colour
    )
    st.plotly_chart(fig, use_container_width=True)

# Life Expectancy chart
with col2:
    fig = make_line_chart(
        'Life expectancy at birth (years)',
        'Life Expectancy',
        selected_country,
        selected_compare,
        primary_colour,
        compare_colour
    )
    st.plotly_chart(fig, use_container_width=True)

# Under-5 Mortality chart
with col3:
    fig = make_line_chart(
        'Under-five mortality rate',
        'Under-5 Mortality Rate',
        selected_country,
        selected_compare,
        primary_colour,
        compare_colour
    )
    st.plotly_chart(fig, use_container_width=True)

# Youth Unemployment chart
with col4:
    fig = make_line_chart(
        'Youth unemployment rate (%)',
        'Youth Unemployment Rate',
        selected_country,
        selected_compare,
        primary_colour,
        compare_colour
    )
    st.plotly_chart(fig, use_container_width=True)