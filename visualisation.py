import pandas as pd
import altair as alt
import geopandas as gpd

# Load the data from the cleaned Excel file
file_path = 'OECD_betterLifeIndex_cleaned.xlsx'

# First DataFrame for Comparative Country Overview
dataframe1 = pd.read_excel(file_path, header=None, skiprows=7, usecols="A,H,O,V,X", names=['Country',
                                                                                           'Household Net Wealth (USD)',
                                                                                           'Student Skills (Average Score)',
                                                                                           'Self-Reported Health (%)',
                                                                                           'Feeling Safe Alone At Night (%)'], nrows=42)

# Add country names of non-OECD countries
dataframe1.at[39, 'Country'] = "Brazil"
dataframe1.at[40, 'Country'] = "Russia"
dataframe1.at[41, 'Country'] = "South Africa"

# New column 'OECD Status' to identify OECD and non-OECD countries
dataframe1['OECD Status'] = dataframe1['Country'].apply(lambda x: 'Non-OECD' if x in ['Brazil', 'Russia', 'South Africa'] else 'OECD')

# New column for full country names
dataframe1['Full Country Name'] = dataframe1['Country']

# Create a dictionary to keep track of duplicates
duplicates = {}

# Create a list for x-axis labelling
country_names = []

# Iterate to shorten country names
for i, country in enumerate(dataframe1['Country']):
    # Take the first 3 letters and convert to uppercase

    if country == 'United Kingdom':
        short_name = 'UK'

    elif country == 'United States':
        short_name = 'USA'

    elif country == 'Austria':
        short_name = 'AUT'

    elif country == 'Slovak Republic':
        short_name = 'SVK'

    elif country == 'New Zealand':
        short_name = 'NZ'

    else:
        short_name = country[:3].upper()

    # Update the DataFrame
    dataframe1.at[i, 'Country'] = short_name

    # Append "short_name : country" to country_names list
    country_names.append(f"{short_name} : {country}")

# Set the size domain for size of points
size_domain = [min(dataframe1['Self-Reported Health (%)']), max(dataframe1['Self-Reported Health (%)'])]

# Scatter plot
scatter_plot = alt.Chart(dataframe1).mark_point(filled=True).encode(
    x=alt.X('Household Net Wealth (USD):Q', scale=alt.Scale(domain=[0, 950000])),
    y=alt.Y('Student Skills (Average Score):Q', scale=alt.Scale(domain=[390, 530])),
    size=alt.Size('Self-Reported Health (%):Q', scale=alt.Scale(domain=size_domain, range=(50, 200)),
                   legend=alt.Legend(symbolSize=1, labelFontSize=7)),
    color=alt.Color('Feeling Safe Alone At Night (%):Q',
                    legend=alt.Legend(symbolSize=1, labelFontSize=7, gradientLength=40)),
    shape=alt.Shape('OECD Status:N',
                    scale=alt.Scale(domain=['OECD', 'Non-OECD'], range=['circle', 'square']),
                    legend=alt.Legend(symbolSize=10, labelFontSize=7)),
    tooltip=[alt.Tooltip('Full Country Name', title='Country'), 'Household Net Wealth (USD)',
             'Student Skills (Average Score)', 'Self-Reported Health (%)',
             'Feeling Safe Alone At Night (%)']
).properties(
    width=350,
    height=200,
    title='Comparative Country Overview - Income, Education, Health and Safety'
)

# Add text labels to points
text_labels = alt.Chart(dataframe1).mark_text(
    align='center',
    baseline='top',
    fontSize=5,
    dx=0,
    dy=6,
    angle=0
).encode(
    x=alt.X('Household Net Wealth (USD):Q', scale=alt.Scale(domain=[0, 950000])),
    y=alt.Y('Student Skills (Average Score):Q', scale=alt.Scale(domain=[390, 530])),
    text='Country',
    tooltip=[alt.Tooltip('Full Country Name', title='Country'), alt.Tooltip('Household Net Wealth (USD)'),
                 alt.Tooltip('Student Skills (Average Score)'), alt.Tooltip('Self-Reported Health (%)'),
                 alt.Tooltip('Feeling Safe Alone At Night (%)')]

)

# Combine the scatter plot and text labels
final_chart1 = alt.layer(scatter_plot, text_labels).resolve_scale(
    color='independent',
    size='independent',
    shape='independent'
).properties(
    width=450,
    height=180,
    title='Comparative Country Overview - Income, Education, Health and Safety'
)

# Second DataFrame for Socioeconomic Indicators Across Countries
dataframe2 = pd.read_excel(file_path, header=None, skiprows=7, usecols="A,G,J,N,W", names=['Country',
                                                                                           'Disposable Income (USD)',
                                                                                           'Employment Rate (%)',
                                                                                           'Education Attainment (%)',
                                                                                           'Life Satisfaction (Average Score)'], nrows=42)

# Add country names of non-OECD countries
dataframe2.at[39, 'Country'] = "Brazil"
dataframe2.at[40, 'Country'] = "Russia"
dataframe2.at[41, 'Country'] = "South Africa"

# Adding a new column 'OECD Status' to identify OECD and non-OECD countries
dataframe2['OECD Status'] = dataframe2['Country'].apply(lambda x: 'Non-OECD' if x in ['Brazil', 'Russia',
                                                                                      'South Africa'] else 'OECD')

# Set the size domain to match the range of 'Life Satisfaction (Average Score)'
size_domain = [min(dataframe2['Life Satisfaction (Average Score)']),
               max(dataframe2['Life Satisfaction (Average Score)'])]

# Bar Chart
bar_chart = alt.Chart(dataframe2).mark_bar().encode(
    x='Country:N',
    y='Disposable Income (USD):Q',
    color=alt.Color('Education Attainment (%)', legend=alt.Legend(gradientLength=50)),
    size=alt.Size('Life Satisfaction (Average Score):Q', scale=alt.Scale(range=(1, 8), domain=size_domain)),
    tooltip=['Country', 'Disposable Income (USD)', 'Employment Rate (%)', 'Education Attainment (%)',
             'Life Satisfaction (Average Score)']
).properties(
    title='Socioeconomic Indicators Across Countries',
    width=380,
    height=130
)

# Adding labels above non-OECD bars
labels = alt.Chart(dataframe2[dataframe2['OECD Status'] == 'Non-OECD']).mark_text(
    align='center',
    baseline='top',
    fontSize=5,
    dx=15,
    dy=-2,
    angle=270
).encode(
    x='Country:N',
    y='Disposable Income (USD):Q',
    text='OECD Status'
)

# Combine the bar chart and labels
final_chart2 = (bar_chart + labels).resolve_scale(color='independent', size='independent')


# Third DataFrame for Environmental Indicators by Country
dataframe3 = pd.read_excel(file_path, header=None, skiprows=7, usecols="A,Q,R", names=['Country',
                                                                                        'Air Pollution (µg/m3)',
                                                                                        'Water Quality (%)'], nrows=42)

# Add country names of non-OECD countries
dataframe3.at[39, 'Country'] = "Brazil"
dataframe3.at[40, 'Country'] = "Russia"
dataframe3.at[41, 'Country'] = "South Africa"

# Create Altair chart
base = alt.Chart(dataframe3).encode(
    x='Country:N',
    tooltip=['Country', 'Water Quality (%)', 'Air Pollution (µg/m3)']
)

# Bar chart for Water Quality with blue axis
bar = base.mark_bar(opacity=0.7, color='#1f77b4').encode(
    y=alt.Y('Water Quality (%):Q', axis=alt.Axis(titleColor='#1f77b4', tickColor='#1f77b4',
                                                 labelColor='#1f77b4', domainColor='#1f77b4'))  # Blue axis
)

# Line chart for Air Pollution with red axis
line = base.mark_line(opacity=0.7, color='#e20000').encode(
    y=alt.Y('Air Pollution (µg/m3):Q', axis=alt.Axis(titleColor='#e20000', tickColor='#e20000',
                                                     labelColor='#e20000', domainColor='#e20000'))  # Red axis
)

# Combine the bar and line charts
final_chart3 = alt.layer(bar, line).resolve_scale(
    y='independent'
).properties(
    width=450,
    height=130,
    title='Environmental Factor Comparison by Country'
)


# Fourth DataFrame for Supported Networks Worldwide
dataframe4 = pd.read_excel(file_path, header=None, skiprows=7, usecols="A,M", names=['Country',
                                                                                    'Quality of Support Network (%)'],
                                                                                    nrows=42)

# Add country names of non-OECD countries
dataframe4.at[39, 'Country'] = "Brazil"
dataframe4.at[40, 'Country'] = "Russia"
dataframe4.at[41, 'Country'] = "South Africa"

# Read the cartography data
url = "https://naciscdn.org/naturalearth/110m/cultural/ne_110m_admin_0_countries.zip"
countries_shape = gpd.read_file(url)
countries_shape = countries_shape[['NAME', 'CONTINENT', 'ISO_A3', 'geometry']]

# Filter out Antarctica
countries_shape = countries_shape[countries_shape['NAME'] != 'Antarctica']

# Merge the DataFrames based on country names or codes
merged_data = pd.merge(countries_shape, dataframe4, left_on='NAME', right_on='Country', how='left')

# Create the map
base_map = alt.Chart(countries_shape).mark_geoshape(
    fill='lightgray',
    stroke='white'
).properties(
    width=450,
    height=200
)

# Colour the map based on the "Quality of Support Network (%)"
coloured_map = alt.Chart(merged_data).mark_geoshape().encode(
    alt.Color('Quality of Support Network (%):Q', scale=alt.Scale(scheme='viridis'),
              legend=alt.Legend(offset=0, orient='right', title='Quality of Support Network (%)')),
    tooltip=['Country:N', 'Quality of Support Network (%):Q']
)

# Combine the base map and the coloured map
final_map = base_map + coloured_map

# Add title to the map
final_chart4 = final_map.properties(title='Global Quality of Communities')

# Creating a title for the page
title = alt.Title(
    'Global Well-Being Explorer: Unveiling the OECD Better Life Index',
    anchor='middle',
    offset=10,
    fontSize=16,
    fontWeight='bold',
    fontStyle='italic'
)

# Concatenate the charts
combined_charts = alt.vconcat(
    alt.hconcat(final_chart3, final_chart1, spacing=35),
    alt.hconcat(final_chart2, final_chart4, spacing=5),
    spacing=10,
    title=title
).resolve_scale(
    color='independent',
    size='independent'
)

# Make the entire concatenated chart interactive
combined_charts = combined_charts.interactive()

# Save the combined layout as an HTML file
combined_charts.save('charts.html')
