import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page title and wide layout
st.set_page_config(page_title="Regional Comparison", layout="wide")

df = pd.read_csv("WB_HCP_WIDEF.csv")

# Define the indicators we need =
indicators = [
    'Human Capital Index (HCI) (scale 0-1)',
    'Life expectancy at birth (years)',
    'Under-five mortality rate',
    'Youth unemployment rate (%)'
]

# Keep only rows for selected indicators
df = df[df['INDICATOR_LABEL'].isin(indicators)]

# Define year columns to extract (2000-2023)
year_cols = [str(y) for y in range(2000, 2024)]

# Melt from wide to long format for Plotly
# Keep SEX_LABEL for gender filtering
df_melted = df.melt(
    id_vars=['REF_AREA_LABEL', 'INDICATOR_LABEL', 'SEX_LABEL'],
    value_vars=year_cols,
    var_name='Year',
    value_name='Value'
)

# Convert Year to integer and drop missing values
df_melted['Year'] = df_melted['Year'].astype(int)
df_melted = df_melted.dropna(subset=['Value'])

# Map each country to its region for grouping
region_map = {
    'Afghanistan': 'Asia', 'Albania': 'Europe', 'Algeria': 'Africa',
    'Angola': 'Africa', 'Argentina': 'South America', 'Armenia': 'Asia',
    'Australia': 'Oceania', 'Austria': 'Europe', 'Azerbaijan': 'Asia',
    'Bahrain': 'Asia', 'Bangladesh': 'Asia', 'Belarus': 'Europe',
    'Belgium': 'Europe', 'Benin': 'Africa', 'Bolivia': 'South America',
    'Bosnia and Herzegovina': 'Europe', 'Botswana': 'Africa',
    'Brazil': 'South America', 'Bulgaria': 'Europe', 'Burkina Faso': 'Africa',
    'Burundi': 'Africa', 'Cambodia': 'Asia', 'Cameroon': 'Africa',
    'Canada': 'North America', 'Central African Republic': 'Africa',
    'Chad': 'Africa', 'Chile': 'South America', 'China': 'Asia',
    'Colombia': 'South America', 'Congo, Dem. Rep.': 'Africa',
    'Congo, Rep.': 'Africa', 'Costa Rica': 'North America',
    "Cote d'Ivoire": 'Africa', 'Croatia': 'Europe', 'Cuba': 'North America',
    'Czech Republic': 'Europe', 'Denmark': 'Europe', 'Djibouti': 'Africa',
    'Dominican Republic': 'North America', 'Ecuador': 'South America',
    'Egypt, Arab Rep.': 'Africa', 'El Salvador': 'North America',
    'Estonia': 'Europe', 'Ethiopia': 'Africa', 'Finland': 'Europe',
    'France': 'Europe', 'Gabon': 'Africa', 'Gambia, The': 'Africa',
    'Georgia': 'Asia', 'Germany': 'Europe', 'Ghana': 'Africa',
    'Greece': 'Europe', 'Guatemala': 'North America', 'Guinea': 'Africa',
    'Haiti': 'North America', 'Honduras': 'North America', 'Hungary': 'Europe',
    'India': 'Asia', 'Indonesia': 'Asia', 'Iran, Islamic Rep.': 'Asia',
    'Iraq': 'Asia', 'Ireland': 'Europe', 'Israel': 'Asia',
    'Italy': 'Europe', 'Jamaica': 'North America', 'Japan': 'Asia',
    'Jordan': 'Asia', 'Kazakhstan': 'Asia', 'Kenya': 'Africa',
    'Korea, Rep.': 'Asia', 'Kuwait': 'Asia', 'Kyrgyz Republic': 'Asia',
    'Lao PDR': 'Asia', 'Latvia': 'Europe', 'Lebanon': 'Asia',
    'Lesotho': 'Africa', 'Liberia': 'Africa', 'Lithuania': 'Europe',
    'Madagascar': 'Africa', 'Malawi': 'Africa', 'Malaysia': 'Asia',
    'Mali': 'Africa', 'Mauritania': 'Africa', 'Mauritius': 'Africa',
    'Mexico': 'North America', 'Moldova': 'Europe', 'Mongolia': 'Asia',
    'Morocco': 'Africa', 'Mozambique': 'Africa', 'Myanmar': 'Asia',
    'Namibia': 'Africa', 'Nepal': 'Asia', 'Netherlands': 'Europe',
    'New Zealand': 'Oceania', 'Nicaragua': 'North America', 'Niger': 'Africa',
    'Nigeria': 'Africa', 'Norway': 'Europe', 'Pakistan': 'Asia',
    'Panama': 'North America', 'Papua New Guinea': 'Oceania',
    'Paraguay': 'South America', 'Peru': 'South America', 'Philippines': 'Asia',
    'Poland': 'Europe', 'Portugal': 'Europe', 'Romania': 'Europe',
    'Russian Federation': 'Europe', 'Rwanda': 'Africa',
    'Saudi Arabia': 'Asia', 'Senegal': 'Africa', 'Sierra Leone': 'Africa',
    'Singapore': 'Asia', 'Slovak Republic': 'Europe', 'Slovenia': 'Europe',
    'Somalia': 'Africa', 'South Africa': 'Africa', 'South Sudan': 'Africa',
    'Spain': 'Europe', 'Sri Lanka': 'Asia', 'Sudan': 'Africa',
    'Sweden': 'Europe', 'Switzerland': 'Europe', 'Syria': 'Asia',
    'Tajikistan': 'Asia', 'Tanzania': 'Africa', 'Thailand': 'Asia',
    'Togo': 'Africa', 'Trinidad and Tobago': 'North America', 'Tunisia': 'Africa',
    'Turkey': 'Asia', 'Turkmenistan': 'Asia', 'Uganda': 'Africa',
    'Ukraine': 'Europe', 'United Arab Emirates': 'Asia',
    'United Kingdom': 'Europe', 'United States': 'North America',
    'Uruguay': 'South America', 'Uzbekistan': 'Asia', 'Venezuela, RB': 'South America',
    'Vietnam': 'Asia', 'Yemen, Rep.': 'Asia', 'Zambia': 'Africa',
    'Zimbabwe': 'Africa'
}

# Add region column to dataframe
df_melted['Region'] = df_melted['REF_AREA_LABEL'].map(region_map)
df_melted = df_melted.dropna(subset=['Region'])

# Define colour sequences for each type of colour blindness
colour_sequences = {
    "Standard": px.colors.qualitative.Plotly,
    "Deuteranopia (red-green)": ['#000000', '#E69F00', '#56B4E9', '#009E73', '#F0E442'],
    "Protanopia (red-green, dark)": ['#332288', '#117733', '#44AA99', '#88CCEE', '#DDCC77'],
    "Tritanopia (blue-yellow)": ['#CC6677', '#882255', '#AA4499', '#44AA99', '#117733'],
    "Achromatopsia (greyscale)": ['#000000', '#404040', '#808080', '#BFBFBF', '#FFFFFF']
}

# Short descriptions shown to the user for each indicator
indicator_descriptions = {
    'Human Capital Index (HCI) (scale 0-1)': 'The HCI measures how much human capital a child born today can expect to attain by age 18, given the risks of poor health and poor education in their country. A score of 1.0 means full potential reached. A score of 0.5 means only 50% of potential.',
    'Life expectancy at birth (years)': 'The average number of years a newborn is expected to live, given current mortality rates.',
    'Under-five mortality rate': 'The number of children who die before reaching age 5, per 1,000 live births.',
    'Youth unemployment rate (%)': 'The percentage of young people aged 15-24 who are unemployed and actively looking for work.'
}

#SIDEBAR CONTROLS
st.sidebar.title("Controls")

# Dropdown to select which indicator to display
selected_indicator = st.sidebar.selectbox(
    "Select Indicator",
    options=indicators,
    index=0
)

# Only show years that have data for the selected indicator
valid_years = sorted(
    df_melted[df_melted['INDICATOR_LABEL'] == selected_indicator]['Year'].unique().tolist()
)

# Dropdown to select year for bar chart
selected_year = st.sidebar.selectbox(
    "Select Year",
    options=valid_years,
    index=len(valid_years) - 1
)

# Radio button for gender selection
gender = st.sidebar.radio(
    "Gender",
    options=["Total", "Male", "Female"]
)

# Multiselect to filter regions
region_filter = st.sidebar.multiselect(
    "Select Regions",
    options=["Africa", "North America", "South America", "Asia", "Europe", "Oceania"],
    default=["Africa", "North America", "South America", "Asia", "Europe", "Oceania"]
)

# Dropdown to select colour mode 
colour_mode = st.sidebar.selectbox(
    "Colour Mode",
    options=list(colour_sequences.keys())
)

# Get the selected colour sequence
palette = colour_sequences[colour_mode]

st.title("Regional Comparison")
st.markdown(f"*Comparing **{selected_indicator}** across regions ({selected_year})*")
st.info(indicator_descriptions[selected_indicator])

if not region_filter:
    st.warning("Please select at least one region.")
    st.stop()

# Filter data for selected indicator, year, gender and regions
bar_df = df_melted[
    (df_melted['INDICATOR_LABEL'] == selected_indicator) &
    (df_melted['Year'] == selected_year) &
    (df_melted['SEX_LABEL'] == gender) &
    (df_melted['Region'].isin(region_filter))
]

# Group by region and calculate average value
bar_df = bar_df.groupby('Region')['Value'].mean().reset_index()
bar_df.columns = ['Region', 'Average Value']

fig_bar = px.bar(
    bar_df,
    x='Region',
    y='Average Value',
    color='Region',
    title=f'Average {selected_indicator} by Region ({selected_year})',
    labels={'Average Value': selected_indicator},
    color_discrete_sequence=palette
)

# Update layout for dark theme with y axis starting at 0
fig_bar.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    showlegend=False,
    yaxis=dict(rangemode='tozero')  # Always start y axis at 0
)

# Display bar chart
st.plotly_chart(fig_bar, use_container_width=True)

st.subheader(f"{selected_indicator} Over Time by Region")
st.markdown("*How has the regional average changed over time?*")

# Filter data for selected indicator, gender and regions across all years
line_df = df_melted[
    (df_melted['INDICATOR_LABEL'] == selected_indicator) &
    (df_melted['SEX_LABEL'] == gender) &
    (df_melted['Region'].isin(region_filter))
]

# Group by region and year, calculate average
line_df = line_df.groupby(['Region', 'Year'])['Value'].mean().reset_index()
line_df.columns = ['Region', 'Year', 'Average Value']

# Create line chart
fig_line = px.line(
    line_df,
    x='Year',
    y='Average Value',
    color='Region',
    title=f'Regional Average {selected_indicator} Over Time',
    labels={'Average Value': selected_indicator, 'Year': 'Year'},
    color_discrete_sequence=palette
)

# Update layout for dark theme
fig_line.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white',
    legend=dict(bgcolor='rgba(0,0,0,0)'),
    yaxis=dict(rangemode='tozero')
)

# Display line chart
st.plotly_chart(fig_line, use_container_width=True)