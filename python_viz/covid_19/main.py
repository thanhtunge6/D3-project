import pandas as pd
import numpy as np
import plotly.graph_objects as go

data = pd.read_csv("covid_19_data_processed.csv")
months = {1: "January", 2: "February", 3: "March", 4: "April",
          5: "May", 6: "June", 7: "July", 8: "August",
          9: "September", 10: "October", 11: "November", 12: "December"}

data = data.loc[data['year'] == 2020]
data = data.loc[data['Country/Region'].isin(["France", "US", "Russia", "Brazil", "India"])]
data = pd.pivot_table(data, index=['Country/Region', 'month'],values=["Confirmed"],aggfunc=np.sum).reset_index()
data = data.pivot(index='month', columns='Country/Region', values='Confirmed').reset_index()
data["month_text"] = data.apply(lambda row: months[row["month"]], axis=1)
fig = go.Figure()

fig.add_trace(go.Barpolar(
    r=list(data["France"]),
    theta=list(data["month_text"]),
    name="France",
    marker_color='#7A6C5D',
    marker_line_color="black",
    hoverinfo=["all"],
    hovertemplate="%{r} cases",
    opacity=0.7
))
fig.add_trace(go.Barpolar(
    r=list(data["Russia"]),
    theta=list(data["month_text"]),
    name="Russia",
    marker_color='#2A3D45',
    marker_line_color="black",
    hoverinfo=["all"],
    hovertemplate="%{r} cases",
    opacity=0.7
))
fig.add_trace(go.Barpolar(
    r=list(data["Brazil"]),
    theta=list(data["month_text"]),
    name="Brazil",
    marker_color='#DDC9B4',
    marker_line_color="black",
    hoverinfo=["all"],
    hovertemplate="%{r} cases",
    opacity=0.7
))
fig.add_trace(go.Barpolar(
    r=list(data["India"]),
    theta=list(data["month_text"]),
    name="India",
    marker_color='#BCAC9B',
    marker_line_color="black",
    hoverinfo=["all"],
    hovertemplate="%{r} cases",
    opacity=0.7
))
fig.add_trace(go.Barpolar(
    r=list(data["US"]),
    theta=list(data["month_text"]),
    name="US",
    marker_color='#C17C74',
    marker_line_color="black",
    hoverinfo=["all"],
    hovertemplate="%{r} cases",
    opacity=0.7
))
fig.update_layout(
    title="Number of comfirmed Covid 19 cases per month of the top 5 countries in 2020",
    font_size=12,
    legend_font_size=15,
    polar_angularaxis_rotation=90,
    width=900,
    height=900,

    polar=dict(
        bgcolor="rgb(223,223,223)",
        angularaxis=dict(
            linewidth=3,
            showline=True,
            linecolor="black"
        ),
        radialaxis=dict(
            showline=True,
            linewidth=2,
            gridcolor="white",
            gridwidth=2
        )
    )
)
fig.show()
fig.write_html("covid_19.html")