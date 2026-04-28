import streamlit as st
import pandas as pd
import plotly.express as px

# Set page title and wide layout
st.set_page_config(page_title="Scatter Plot", layout="wide")

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
    'Current health expenditure (% of GDP)',
    'Expected Years of School',
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

# ---- GET VALID YEARS ----
# Only show years where all three indicators have data
school_years = set(df_melted[df_melted['INDICATOR_LABEL'] == 'Expected Years of School']['Year'].unique())
life_years = set(df_melted[df_melted['INDICATOR_LABEL'] == 'Life expectancy at birth (years)']['Year'].unique())
mortality_years = set(df_melted[df_melted['INDICATOR_LABEL'] == 'Under-five mortality rate']['Year'].unique())

# Intersection gives us years where all three have data
valid_years = sorted(school_years & life_years & mortality_years)

# ---- REGION MAPPING ----
# Map each country to its region for colour coding
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

# ---- COLOUR PALETTES ----
# Define colour sequences for each type of colour blindness
colour_sequences = {
    "Standard": px.colors.qualitative.Plotly,
    "Deuteranopia (red-green)": ['#000000', '#E69F00', '#56B4E9', '#009E73', '#F0E442'],
    "Protanopia (red-green, dark)": ['#332288', '#117733', '#44AA99', '#88CCEE', '#DDCC77'],
    "Tritanopia (blue-yellow)": ['#CC6677', '#882255', '#AA4499', '#44AA99', '#117733'],
    "Achromatopsia (greyscale)": ['#000000', '#404040', '#808080', '#BFBFBF', '#FFFFFF']
}

# ---- SIDEBAR CONTROLS ----
st.sidebar.title("Controls")

# Dropdown to select year - only shows years with data for all three indicators
scatter_year = st.sidebar.selectbox(
    "Select Year",
    options=valid_years,
    index=len(valid_years) - 1
)

# Dropdown to select colour mode for accessibility
colour_mode = st.sidebar.selectbox(
    "Colour Mode",
    options=list(colour_sequences.keys())
)

# Multiselect to filter by region
region_filter = st.sidebar.multiselect(
    "Filter by Region",
    options=["Africa", "North America", "South America", "Asia", "Europe", "Oceania"],
    default=["Africa", "North America", "South America", "Asia", "Europe", "Oceania"]
)

# Get the selected colour sequence
colour_seq = colour_sequences[colour_mode]

# ---- PAGE TITLE ----
st.title("Education vs Life Expectancy")
st.markdown("*Do countries where children spend more years in school have longer life expectancy?*")

# ---- BUILD SCATTER DATA ----
# Get each indicator separately then merge on country name
school = df_melted[
    (df_melted['INDICATOR_LABEL'] == 'Expected Years of School') &
    (df_melted['Year'] == scatter_year)
][['REF_AREA_LABEL', 'Value']].rename(columns={'Value': 'School Years'})

life_exp = df_melted[
    (df_melted['INDICATOR_LABEL'] == 'Life expectancy at birth (years)') &
    (df_melted['Year'] == scatter_year)
][['REF_AREA_LABEL', 'Value']].rename(columns={'Value': 'Life Expectancy'})

mortality = df_melted[
    (df_melted['INDICATOR_LABEL'] == 'Under-five mortality rate') &
    (df_melted['Year'] == scatter_year)
][['REF_AREA_LABEL', 'Value']].rename(columns={'Value': 'Under5 Mortality'})

# Merge all three indicators into one dataframe
scatter_df = school.merge(life_exp, on='REF_AREA_LABEL').merge(mortality, on='REF_AREA_LABEL')

# Add region column using region map
scatter_df['Region'] = scatter_df['REF_AREA_LABEL'].map(region_map).fillna('Other')

# Apply region filter
scatter_df = scatter_df[scatter_df['Region'].isin(region_filter)]

# ---- SCATTER PLOT ----
fig_scatter = px.scatter(
    scatter_df,
    x='School Years',
    y='Life Expectancy',
    size='Under5 Mortality',
    color='Region',
    hover_name='REF_AREA_LABEL',
    title=f'Education vs Life Expectancy ({scatter_year})',
    labels={
        'School Years': 'Expected Years of School',
        'Life Expectancy': 'Life Expectancy (years)',
        'Under5 Mortality': 'Under-5 Mortality Rate'
    },
    size_max=40,
    opacity=0.7,
    color_discrete_sequence=colour_seq
)

# Update layout for dark theme
fig_scatter.update_layout(
    height=600,
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font_color='white'
)

# Display the scatter plot
st.plotly_chart(fig_scatter, use_container_width=True)