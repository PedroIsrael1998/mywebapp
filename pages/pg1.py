
#1.1 Import libraries
#basic libraries:
import pandas as pd
# import os
import numpy as np

#date alteration:
# import datetime as dt
# import xlrd

#progress bar
# from time import sleep
# from tqdm.auto import tqdm, trange
    # The .auto library detects if you are on anotebook. If so, it will show a better progress bar than if you were on a script. 
    #for more info write: help(tqdm) or go to website.

#approximate match:
# import fuzzywuzzy
# from fuzzywuzzy import process
# import chardet

#geo libraries:
# import geopandas as gpd

# dash: 
import dash
from dash import Dash,dcc, html, callback, Output, Input
import dash_bootstrap_components as dbc                       
import dash_mantine_components as dmc


# #graphs:
# import matplotlib.pyplot as plt
# import seaborn as sns
# #plotly express:
import plotly.express as px
import plotly.graph_objects as go

# ------------------------------------------------------------------------------

# Web tab info:
# To create meta tag for each page, define the title, image, and description.
dash.register_page(__name__,
                   path='/',  # '/' is home page and it represents the url
                   name='Economic Statistics',  # name of page, commonly used as name of link
                   title='Index',  # title that appears on browser's tab
                   image='pg1.png',  # image in the assets folder # Improvement: Must change this image
                   description='Economic Statistics'
)

# ------------------------------------------------------------------------------
#dfs:
agriculture_GDP = pd.read_csv('/Users/peisrael2201/Desktop/climate/agr.csv')
gapminder = px.data.gapminder()
tips = px.data.tips()
carshare = px.data.carshare()
# ------------------------------------------------------------------------------
figure_templates = [
    "plotly",
    "ggplot2",
    "seaborn",
    "simple_white",
    "plotly_white",
    "plotly_dark",
    "presentation",
    "xgridoff",
    "ygridoff",
    "gridon",
    "none",
]
# ------------------------------------------------------------------------------
change_figure_template = html.Div(
    [
        html.Div("Change Figure Template"),
        dcc.Dropdown(figure_templates, figure_templates[3], id="template"),
    ],
    className="pb-4",
)


layout = dbc.Container(
    [
        dbc.Row(dbc.Col(change_figure_template, lg=6)),
        dbc.Row(dbc.Col(html.Div(id="graphs"))),
    ],
    className="dbc p-4",
    fluid=True,
)
# ------------------------------------------------------------------------------

@callback(
    Output("graphs", "children"),
    Input("template", "value"),
)

# ------------------------------------------------------------------------------

def update_graph_theme(template):

    # ----------------------
    scatter_graph= px.scatter(
            agriculture_GDP,
            x="GDP_current_UsBillDollars",
            y="Agriculture_percent",
            color="Continent",
            title=f"Top Countries on Agriculture % of GDP (value added, 2021)  <br>{template} figure template",
            template=template,
        )

    # Alter hover values:
    scatter_graph.update_traces(
        text=agriculture_GDP['Country'],
        hovertemplate="<b>%{text}</b><br><br>" +
        "Agriculture %: (% of GDP): %{y}<br>" +
        "GDP: %{x}<br>" +
        "<extra></extra>",
    )

    # we must create a dcc.Graph object with the graph to display it:
    graph1 = dcc.Graph(figure=scatter_graph,className="border")

    # ----------------------

    graph2 = dcc.Graph(
        figure=px.scatter(
            gapminder,
            x="gdpPercap",
            y="lifeExp",
            size="pop",
            color="continent",
            hover_name="country",
            animation_frame="year",
            animation_group="country",
            log_x=True,
            size_max=60,
            title=f"Life Expectancy VS. (GDP per capita & Population) <br>{template} figure template",
            template=template,
            # raise height:
            height=600,
            # set y start from 0-90:
            range_y=[0, 90],
        ),
        className="border",
    )
    # ----------------------
    graph3 = dcc.Graph(
        figure=px.violin(
            tips,
            y="tip",
            x="smoker",
            color="sex",
            box=True,
            points="all",
            hover_data=tips.columns,
            title=f"Tip Analysis by Sex & Smoker <br>{template} figure template",
            template=template,
        ),
        className="border",
    )
    # ----------------------
    graph4 = dcc.Graph(
        figure=px.scatter_mapbox(
            carshare,
            lat="centroid_lat",
            lon="centroid_lon",
            color="peak_hour",
            size="car_hours",
            size_max=15,
            zoom=10,
            mapbox_style="carto-positron",
            title=f"Carshare in Montreal <br> {template} figure template",
            template=template,
        ),
        className="border",
    )
    # ----------------------
    return [
        #------------
        # Page break: 
        html.Div(children= "",style={ 'margin-bottom': '0px','margin-top': '15px'}),
        #------------
        dbc.Row(graph2),
        #------------
        dbc.Row([dbc.Col(graph3, lg=6), dbc.Col(graph4, lg=6)], className="mt-4"),
        #------------
        # Page break: 
        html.Div(children= "",style={ 'margin-bottom': '0px','margin-top': '15px'}),
        #------------
        dbc.Row(graph1),
        #------------
    ]


