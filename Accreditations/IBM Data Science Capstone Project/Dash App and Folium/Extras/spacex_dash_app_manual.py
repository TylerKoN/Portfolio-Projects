# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(id='site-dropdown',
                                             options = [
                                                 {'label': 'All Sites', 'value': 'ALL'},
                                                 {'label': 'CCAFS LC-40', 'value': 'CCAFS LC-40'},
                                                 {'label': 'KSC LC-39A', 'value': 'KSC LC-39A'},
                                                 {'label': 'VAFB SLC-4E', 'value': 'VAFB SLC-4E'},
                                                 {'label': 'CCAFS SLC-40', 'value': 'CCAFS SLC-40'}
                                             ],
                                             value = 'ALL',
                                             placeholder = "Select a Launch Site here",
                                             searchable = True
                                             ),
                                html.Br(),
                                

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),
                                
                                html.P("Payload range (Kg):"),

                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, 
                                                max=10000, 
                                                step=1000,
                                                marks={0: '0', 2500: '2500', 5000: '5000', 7500: '7500', 10000: '10000'},
                                                value=[min_payload, max_payload]),
                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart'))
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(spacex_df, values='class', 
        names='Launch Site', 
        title='Pie Charts of All Successful launch outcomes from each Launch Sites')
        return fig
    elif entered_site == 'CCAFS LC-40':
        fig = px.pie(spacex_df[spacex_df['Launch Site'] == 'CCAFS LC-40'], 
                     names='class', 
                     title='Pie Chart of Successful and Failure of launch outcomes from CCAFS LC-40',
                     labels = {0: 'Failure', 1: 'Success'}
                     )
        return fig
    elif entered_site == 'CCAFS SLC-40':
        fig = px.pie(spacex_df[spacex_df['Launch Site'] == 'CCAFS SLC-40'], 
                     names='class', 
                     title='Pie Chart of Successful and Failure of launch outcomes from CCAFS SLC-40',
                     labels = {0: 'Failure', 1: 'Success'}
                     )
        return fig
    elif entered_site == 'KSC LC-39A':
        fig = px.pie(spacex_df[spacex_df['Launch Site'] == 'KSC LC-39A'], 
                     names='class', 
                     title='Pie Chart of Successful and Failure of launch outcomes from KSC LC-39A',
                     labels = {0: 'Failure', 1: 'Success'}
                     )
        return fig
    elif entered_site == 'VAFB SLC-4E':
        fig = px.pie(spacex_df[spacex_df['Launch Site'] == 'VAFB SLC-4E'], 
                     names='class', 
                     title='Pie Chart of Successful and Failure of launch outcomes from VAFB SLC-4E',
                     labels = {0: 'Failure', 1: 'Success'}
                     )
        return fig
    
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site2, payload_range):
    min_payload, max_payload = payload_range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= min_payload) & 
                             (spacex_df['Payload Mass (kg)'] <= max_payload)]
    if entered_site2 == 'ALL':
        fig = px.scatter(filtered_df, 
                         x ='Payload Mass (kg)', 
                         y ='class', 
                         title='Scatterplot of Relationship between Payload Mass and Launch Outcome',
                         color = 'Booster Version Category')
        return fig
    elif entered_site2 == 'CCAFS LC-40':
        fig = px.scatter(filtered_df[spacex_df['Launch Site'] == 'CCAFS LC-40'], 
                 x ='Payload Mass (kg)', 
                 y ='class', 
                 title='Scatterplot of Payload Mass and Launch Outcome from CCAFS LC-40', 
                 color = 'Booster Version Category')
        return fig
    elif entered_site2 == 'CCAFS SLC-40':
        fig = px.scatter(filtered_df[spacex_df['Launch Site'] == 'CCAFS SLC-40'], 
                 x ='Payload Mass (kg)', 
                 y ='class', 
                 title='Scatterplot of Payload Mass and Launch Outcome from CCAFS SLC-40', 
                 color = 'Booster Version Category')
        return fig
    elif entered_site2 == 'KSC LC-39A':
        fig = px.scatter(filtered_df[spacex_df['Launch Site'] == 'KSC LC-39A'], 
                 x ='Payload Mass (kg)', 
                 y ='class', 
                 title='Scatterplot of Payload Mass and Launch Outcome from KSC LC-39A', 
                 color = 'Booster Version Category')
        return fig
    elif entered_site2 == 'VAFB SLC-4E':
        fig = px.scatter(filtered_df[spacex_df['Launch Site'] == 'VAFB SLC-4E'], 
                 x ='Payload Mass (kg)', 
                 y ='class', 
                 title='Scatterplot of Payload Mass and Launch Outcome from VAFB SLC-4E', 
                 color = 'Booster Version Category')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()