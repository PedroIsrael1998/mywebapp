#1.1 Libs: 
import pandas as pd

# dash: 
import dash
from dash import Dash,dcc, html, callback, Output, Input
import dash_bootstrap_components as dbc                       
import dash_mantine_components as dmc

# plotly express:
import plotly.express as px
import plotly.graph_objects as go

# ------------------
# 1.2 Create the app
# app = Dash(__name__, pages_folder="") # instead of use_pages=True
app = dash.Dash(__name__, pages_folder="", external_stylesheets=[dbc.themes.SPACELAB]) #SPACELAB = cool formatting for sidebar
server = app.server  # THis is just for heroku or render
#----------
# 2. pages:
#----------
# 2.1 Page 1:
#---------
#dfs:

#make df agriculture_GDP:
agr_data = [
    ['Sierra Leone', 'Africa', 57, 4.0],
    ['Chad', 'Africa', 54, 12.0],
    ['Ethiopia', 'Africa', 38, 111.0],
    ['Liberia', 'Africa', 37, 4.0],
    ['Niger', 'Africa', 36, 15.0],
    ['Mali', 'Africa', 36, 19.0],
    ['Afghanistan', 'Asia', 33, 15.0],
    ['Central African Republic', 'Africa', 30, 3.0],
    ['Mozambique', 'Africa', 27, 16.0],
    ['Tanzania', 'Africa', 26, 68.0],
    ['Guinea', 'Africa', 26, 16.0],
    ['Marshall Islands', 'Oceania', 25, 0.0],
    ['Uzbekistan', 'Asia', 25, 69.0],
    ['Rwanda', 'Africa', 24, 11.0],
    ['Uganda', 'Africa', 24, 41.0],
    ['Myanmar', 'Asia', 23, 65.0],
    ['Nigeria', 'Africa', 23, 441.0],
    ['Cambodia', 'Asia', 23, 27.0],
    ['Malawi', 'Africa', 23, 13.0],
    ['Pakistan', 'Asia', 23, 348.0],
    ['Kenya', 'Africa', 22, 110.0],
    ['Gambia', 'Africa', 22, 2.0]
]
agriculture_GDP = pd.DataFrame(agr_data, columns=['Country', 'Continent', 'Agriculture_percent', 'GDP_current_UsBillDollars'])
agriculture_GDP.index += 1
gapminder = px.data.gapminder()
tips = px.data.tips()
carshare = px.data.carshare()
# ------------------
#pre layout:
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

change_figure_template = html.Div(
    [
        html.Div("Change Figure Template"),
        dcc.Dropdown(figure_templates, figure_templates[3], id="template"),
    ],
    className="pb-4",
)
#------------------
# Web tab info:

dash.register_page(
    "Economic Statistics",
    path='/',  # '/' is home page and it represents the url
    name='Economic Statistics',  # name of page, commonly used as name of link
    # title='Index',  # title that appears on browser's tab
    # image='pg1.png',  # image in the assets folder # Improvement: Must change this image
    # description='Economic Statistics',
    layout= dbc.Container(
        [
            dbc.Row(dbc.Col(change_figure_template, lg=6)),
            dbc.Row(dbc.Col(html.Div(id="graphs"))),
        ],
        className="dbc p-4",
        fluid=True,
    )   
)

#----------
#2.2 Page 2:
#----------
# Necessary functions:

def calc_pop_after_births(initial_pop, birth_rate):
    # Calculate the number of births for the year
    year_births = initial_pop * birth_rate
    # Return the population after births
    return round(initial_pop + year_births,ndigits=0)

def calc_pop_after_deaths(pop_after_births, death_rate):
    # Calculate the number of deaths for the year
    year_deaths = pop_after_births * death_rate
    # Return the population after deaths
    return round(pop_after_births - year_deaths,ndigits=0) 
# ------------------
#DATA:

# Pop density graph:

# Import data: 
df_pop_density = pd.read_csv("https://raw.githubusercontent.com/tolgahancepel/tempdataset/main/population-density.csv")
#filter data::
df_pop_density = df_pop_density[(df_pop_density["Year"] >= 1980) & (df_pop_density["Year"] <= 2030)]
# change column name 'population_density' to 'density':
df_pop_density = df_pop_density.rename(columns={'population_density': 'density'})
#------------------
# Pre layout:

# Make lists for input dropdowns:
output_measures = ['initial_pop','year_births','pop_after_births','year_deaths','pop_after_deaths']
gas_output_measures = ['CO2_emissions_ppm','C02_concentration_ppm','methane_emissions_ppm','methane_concentration_ppm','anual_temp_increment','agg_temp_increment']
# ------------------
# Vars to insert in layout:
    # We do it like this in case we want to use the same layout for the different pages on the future.
not_graphs = html.Div( # I think you can put dbc.Container and it wont change a thing.
    [
        # ------------------
        #Main title:
        html.Div(children= "Population Predictor",style={
            'fontSize':30, 
            'textAlign':'center', 
            'color':'#006400', 
            'margin-bottom': '10px', 
                # blank space below the div. This is the best way to leave blank spaces. 
            'margin-top': '0px'
                # blank space above the div
        }),

        # ------------------
        #Input boxes:
        # Tiles: 
        dbc.Row([
            dbc.Col(html.Div(children= "Initial population in mill (global 2020 = 8000)",style={'fontSize':15, 'textAlign':'left'})),
            dbc.Col(html.Div(children= "Birth Rate (0.025)",style={'fontSize':15, 'textAlign':'left'})),
            dbc.Col(html.Div(children= "Death Rate (0.0075)",style={'fontSize':15, 'textAlign':'left'})),
        ]),

        #Boxes: 
        dbc.Row([

            #Initial population:
            dbc.Col([
                dcc.Input(
                    id="initial_pop",
                    type="number",
                    min=0,
                    value=8000,
                    step=1,
                    size="lg",
                    style={"font-size": "1.6rem"},
                    className="mb-3",
                )
            ], xs=10, sm=10, md=8, lg=4, xl=4, xxl=4),
        
            # Birth rate:
            dbc.Col([
                dcc.Input(
                    id="birth_rate",
                    type="number",
                    min=0,
                    value= 0.025,
                    step=0.001, 
                    size="lg",
                    style={"font-size": "1.6rem"},
                    className="mb-3",
                )
            ], xs=10, sm=10, md=8, lg=4, xl=4, xxl=4),

            # Death rate:
            dbc.Col([
                dcc.Input(
                    id="death_rate",
                    type="number",
                    min=0,
                    value= 0.0075,
                    step=0.0001,
                    size="lg",
                    style={"font-size": "1.6rem"},
                    className="mb-3",
                )
            ], xs=10, sm=10, md=8, lg=4, xl=4, xxl=4)

        ]),
        
        # ------------------
        # Page break: 
        html.Div(children= "",style={ 'margin-bottom': '0px','margin-top': '10px'}),
            #THis is the best way to do a page break as you can regulate the size of the break. These 2 other option always leave the same amount of space: 
            # html.Br(),
            # html.P(),

        # ------------------
        #Population vars:
        #title:
        html.Div(children= "Choose the Population Variables you want to display",style={'fontSize':15, 'textAlign':'left', 'margin-bottom': '0px','margin-top': '0px'}),

        #dropdown:
        dcc.Dropdown(
            id="output_measure",
            value='pop_after_deaths',
            options=output_measures,
            multi=True, # True allows multiple selection
        ),

        # ------------------
        # Page break: 
        html.Div(children= "",style={ 'margin-bottom': '0px','margin-top': '15px'}),
        # ------------------
        # Gas vars:

        #title:
        html.Div(children= "Choose the Gas/temp Variables you want to display",style={'fontSize':15, 'textAlign':'left'}),

        #dropdown:
        dcc.Dropdown(
            id="gas_output_measure",
            value='agg_temp_increment',
            options=gas_output_measures,
            multi=True, # True allows multiple selection
        ),

        # ------------------
        # Page break: 
        html.Div(children= "",style={ 'margin-bottom': '0px','margin-top': '15px'}),
    ],
    # className="dbc p-4",
    # fluid=True, # fluid=True = Use full width of the container
)
# ------------------
# Web tab info:
dash.register_page(
    "Climate Predictions",
    path='/ClimatePredictions',  # represents the url text
    name='Climate Predictions',  # name of page, commonly used as name of link
    title='Climate Predictions',  # represents the title of browser's tab
    layout=dbc.Container( 
        [   
            # not_graphs: 
            dbc.Row(not_graphs),
            # Graphs:
            dbc.Row(dbc.Col(html.Div(id="graphs2"))),
        ],
        className="dbc p-4", # what does this do?: dbc p-4 = padding 4 (px) on all sides of the container 
        fluid=True, # fluid=True = Use full width of the container
    )
)
#----------
# page 1 Callbacks & def:

#page 1:
@callback(
    Output("graphs", "children"),
    Input("template", "value"),
)
#page 1:
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
            title=f"Tip Analysis by Sex & Smoking habit <br>{template} figure template",
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
    #return:
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
# -------------------
# page 2 Callbacks & def:
#callback pag 2
@callback(
    #outputs:
    Output('graphs2', 'children'), # this will show 3 graphs
    #inputs:
    Input('initial_pop', 'value'),
    Input('birth_rate', 'value'),
    Input('death_rate', 'value'),
    Input('output_measure', 'value'),
    Input('gas_output_measure', 'value'),
)
#Def pag2:
# Make df & pop linegraph:
def update_graph(initial_pop,birth_rate,death_rate,output_measure,gas_output_measure):

    # ----------------
    # Making the df: 

    # intial_pop to units:
    initial_pop = initial_pop * 1000000

    #create empty df:
    df = pd.DataFrame()

    #PREVARS:
        # vars we need to be set before the for loop:
    C02_concentration_ppm = 416.5
    methane_concentration_ppm = 1.9
    agg_temp_increment = 0.00

    # Add rows for years: 2023 - 2030:
    for year in range(2022, 2031):

        # ----------------------------
        # calculate variables for column values: 
            # we do it like this so as not to repeat calcualtions in the columns

        # Calculate the number of years passed since the initial year
        years_passed = year - 2022
        # Calculate the initial population for the year:
        if year == 2022:
            initial_pop = initial_pop
        else:
            initial_pop = df['pop_after_deaths'].iloc[-1]

        # Calculate the population after births and deaths for the year
        pop_after_births = calc_pop_after_births(initial_pop, birth_rate)
        pop_after_deaths = calc_pop_after_deaths(pop_after_births, death_rate)


        #Co2 emissions:
        CO2_emissions_ppm = round(pop_after_deaths * 0.0000000003125, ndigits=2)
            # 2.5 ppm

        # C02_concentration_ppm:
        C02_concentration_ppm += CO2_emissions_ppm 
            # 419 ppm

        #methane_emissions:
        methane_emissions_ppm = round(pop_after_deaths * 0.00000000000125, ndigits=4)
            #40% natural 60% human
            # 0.01 ppm

        #methane_concentration:
        methane_concentration_ppm += methane_emissions_ppm
            # 1.9 ppm
        
        # anual_temp_increment:
        anual_temp_increment = round(pop_after_deaths * 0.00000000016, ndigits=2)
            #1.28 celcius

        #agg_temp_increment:
        agg_temp_increment += anual_temp_increment

        # ----------------------------

        # #make df global:
        # global year_df

        # Create df:
        year_df = pd.DataFrame({
            'Year': [year],
            'years_passed': [years_passed],
            'initial_pop': [initial_pop],
            'year_births': [pop_after_births - initial_pop],
            'pop_after_births': [pop_after_births],
            'year_deaths': [pop_after_births - pop_after_deaths],
            'pop_after_deaths': [pop_after_deaths],
            'CO2_emissions_ppm': CO2_emissions_ppm,
            'C02_concentration_ppm':C02_concentration_ppm,
            'methane_emissions_ppm': methane_emissions_ppm,
            'methane_concentration_ppm': methane_concentration_ppm,
            'anual_temp_increment': anual_temp_increment,
            'agg_temp_increment': agg_temp_increment
        }
        , index = [year-2022])

        # Concatenate the new DataFrame with the existing one
        df = pd.concat([df, year_df])

    # -----------------------------
    # Population linegraph:
        # Improvement: I want all line´s colors to be variations of green. But I couldn´t find a way.
    pop_linegraph = dcc.Graph(
        figure= px.line(
            df,
            x='Year',
            y= output_measure,
            template='simple_white',
                # this template erases the grid lines on the background of the graph
            markers =dict(
                size=10,
                color='red', 
                symbol='circle'  # shape
            ),
            
            # title:
                # Improvement: I want to center title.
            title='Population variables',

            # fixed axis titles:
            labels={
                'Year': 'Year', 
                'value': 'Population',
                'variable': 'Population variables' # it´s a title for the line legends
            },
        ),
        className="border", # adds border around figure.
    )
 
    # -----------------------------
    # Gases linegraph: 
    figure1= px.line(
        df,
        x='Year',
        y= gas_output_measure,
        template='simple_white',
            # this template erases the grid lines on the background of the graph
        markers =dict(
            size=10,
            color='red', 
            symbol='circle'  # shape
        ),
        # title:
            # Improvement: I want to center title.
        title=' Gas / Temp  variables',
        # fixed axis titles:
        labels={
            'Year': 'Year', 
            'value': 'Value',
            'variable': 'Gas / Temp  variables' # it´s a title for the line legends
        },
    )
        
    if 'agg_temp_increment' in gas_output_measure:
        # display a red line at y=5 (celcius) showing the max temp the planet can allow: 
        # If agg_temp_increment = 5 , then the world will be uninhabitable
        # Imporvement: We should add a value label to the line for the user to understand what it means
        figure1.add_shape(
            type="line",
            x0=2022,
            y0=5,
            x1=2030,
            y1=5,
            line=dict(
                color="DarkRed",
                width=3,
                dash="solid",
            )
        )

    # we must create a dcc.Graph object with the graph to display it:
    gas_linegraph = dcc.Graph(figure=figure1,className="border") # adds border around figure

    # -----------------------------
    # Density choropleth map:

    #graph:
    choropleth_fig = px.choropleth(
        data_frame=df_pop_density,
        title= "Population density (per km2)",
        locations="Code",
        color="density",
        hover_name="Entity",
        animation_frame="Year",
        range_color=[df_pop_density.density.min(), 200],
        # white to red:
        color_continuous_scale="reds",
    )
    # ----------------------
    # alter layout
    choropleth_fig.update_layout(
        height=900,
        #center title:
        title_x=0.5,
        # change title font:
        title_font=dict(
            family="Verdana",
            size=20,
            #dark red:
            color="#8b0000"
        ),
        #remove color bar:
        coloraxis_showscale=False,

        # alter starting position:
        geo=dict(
            projection_scale=100,
            center=dict(lat=0, lon=0),
            showframe=False,
            showcoastlines=False,
            showland=False,
        )
    )
    # ----------------------
    # alter animation:
    choropleth_fig.layout.updatemenus[0].buttons[0].args[1]["frame"]["duration"] = 70
    # ----------------------
    # alter geo fitbounds:
    choropleth_fig.update_geos(
        fitbounds="locations",
        # ocean color = light blue:
        bgcolor="#e6f0ff",
    )
    # ----------------------

    # we must create a dcc.Graph object with the graph to display it:
    density_choroplethmap = dcc.Graph(figure=choropleth_fig,className="border") # adds border around figure
    # -----------------------------
    #return:
    return [
        # population linegraph:
        dbc.Row(pop_linegraph), 
        # -----------------------------
        # Page break: 
        html.Div(children= "",style={ 'margin-bottom': '0px','margin-top': '15px'}),
        # -----------------------------
        # gas linegraph:
        dbc.Row(gas_linegraph),
        # -----------------------------
        # Page break: 
        html.Div(children= "",style={ 'margin-bottom': '0px','margin-top': '15px'}),
        # -----------------------------
        # gas linegraph:
        dbc.Row(density_choroplethmap),
        # -----------------------------
    ]

# -----------------------------
#5. general page pre layout: 
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
# -------------------
# 6. general page layout: 

app.layout = dbc.Container([
    
    #title:
    dbc.Row([
        # color blue
        html.Div(children="My projects",style={'fontSize':50, 'textAlign':'center', 'color':'#1E90FF'})
    ]),
    
    # line break:
    html.Hr(),

    #sidebar & page container:
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
# -------------------
# 7. run:
if __name__ == '__main__':
    app.run_server(debug=True) # debug=False means that the app will not restart when you make changes to the code. YOu must change it to True when in Render mode

# -------------------




