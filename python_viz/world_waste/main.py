import pandas as pd
import numpy as np
import plotly.express as px

data = {"region": [],
        "parent": [],
        "Tons of municipal solid waste": []}

regions_name = {"ECS": "Europe & Central Asia",
                "MEA": "Middle East & North Africa",
                "EAS": "East Asia & Pacific",
                "NAC": "North America",
                "SAS": "South Asia",
                "LCN": "Latin America & Caribbean",
                "SSF": "Sub-Saharan Africa"}

color_maps = {
    'World': 'white',
    "Europe & Central Asia": "#333333",
    "Middle East & North Africa": "#666A86",
    "East Asia & Pacific": "#95B8D1",
    "North America": "#E8DDB5",
    "South Asia": "#EDAFB8",
    "Latin America & Caribbean": "#F96E46",
    "Sub-Saharan Africa": "#F9C846"
}
country_regions = pd.read_csv("country_level_codebook.csv")
city_region = pd.read_csv("city_level_codebook_0.csv")
country_data = pd.read_csv("country_level_data_0.csv")
city_data = pd.read_csv("city_level_data_0_0.csv")
country_data['total_msw_total_msw_generated_tons_year'] = country_data['total_msw_total_msw_generated_tons_year'].fillna(0)
city_data['total_msw_total_msw_generated_tons_year'] = city_data['total_msw_total_msw_generated_tons_year'].fillna(0)

for i, row in city_data.iterrows():
    data["region"].append(row["city_name"])
    data["parent"].append(row["country_name"])
    data["Tons of municipal solid waste"].append(row["total_msw_total_msw_generated_tons_year"])

for i, row in country_data.iterrows():
    data["region"].append(row["country_name"])
    data["parent"].append(regions_name[row["region_id"]])
    data["Tons of municipal solid waste"].append(row["total_msw_total_msw_generated_tons_year"])

group_by_region = pd.pivot_table(country_data, index=['region_id'],values=["total_msw_total_msw_generated_tons_year"],aggfunc=np.sum).reset_index()

for i, row in group_by_region.iterrows():
    data["region"].append(regions_name[row["region_id"]])
    data["parent"].append("World")
    data["Tons of municipal solid waste"].append(row["total_msw_total_msw_generated_tons_year"])

data["region"].append("World")
data["parent"].append("")
data["Tons of municipal solid waste"].append(group_by_region.sum(axis=0)["total_msw_total_msw_generated_tons_year"])

fig = px.sunburst(
    data,
    names='region',
    parents='parent',
    values='Tons of municipal solid waste',
    hover_data={'region': True, 'Tons of municipal solid waste': ':.1f', "parent": False},
    color='region',
    color_discrete_map=color_maps
)

fig.update_layout(
    title="Which cities/countries are producing the most municipal solid waste per year?",
    font_size=12,
    legend_font_size=15,
    polar_angularaxis_rotation=90,
    width=1200,
    height=1200
)
fig.write_html("msw.html")