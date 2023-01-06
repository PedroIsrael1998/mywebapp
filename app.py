import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
import pandas as pd

app = dash.Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SPACELAB])
server = app.server  # THis is just for heroku or render

sidebar = dbc.Nav(
            [
                dbc.NavLink(
                    [
                        html.Div(page["name"], className="ms-2"),
                    ],
                    href=page["path"],
                    active="exact",
                )
                for page in dash.page_registry.values()
            ],
            vertical=True,
            pills=True,
            className="bg-light",
)

app.layout = dbc.Container([
    #title:
    dbc.Row([
        # color blue
        html.Div(children="My projects",style={'fontSize':50, 'textAlign':'center', 'color':'#1E90FF'})
    ]),
    # line break:
    html.Hr(),

    dbc.Row(
        [
            #sidebar
            dbc.Col(
                [
                    sidebar
                ], xs=4, sm=4, md=2, lg=2, xl=2, xxl=2),
            #page_container:
            dbc.Col(
                [
                    dash.page_container
                ], xs=8, sm=8, md=10, lg=10, xl=10, xxl=10)
        ]
    )
], fluid=True)


if __name__ == "__main__":
    app.run(debug=False)
