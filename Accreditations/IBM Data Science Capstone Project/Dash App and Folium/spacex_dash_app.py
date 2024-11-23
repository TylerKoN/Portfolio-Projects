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
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                html.H4(id='output-1', children=['KSC LC-39A has the largest successful launches']), 
                                html.H4(id='output-2', children=['KSC LC-39A has the highest Successful Launch outcomes']),
                                html.H4(id='output-3', children=['Payload Range between 2000kg to 6000kg has the highest launch success rate']),
                                html.H4(id='output-4', children=['Payload Range between 6000g to 8000kg has the lowest launch success rate']),
                                html.H4(id='output-5', children=['The FT F9 Booster Version has the highest launch success rate'])
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))
def get_pie_chart(entered_site):
    filtered_df = spacex_df
    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Pie Charts of All Successful launch outcomes from each Launch Sites')
        return fig
    elif entered_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == entered_site]
        fig = px.pie(filtered_df, 
                     names='class', 
                     title=f'Pie Chart of Successful and Failure of launch outcomes from {entered_site}',
                     labels = {0: 'Failure', 1: 'Success'}
                     )
        return fig
    
# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'), Input(component_id='payload-slider', component_property='value')])
def get_scatter_chart(entered_site2, payload_range):
    min_payload, max_payload = payload_range
    filtered_df2 = spacex_df[(spacex_df['Payload Mass (kg)'] >= min_payload) & 
                             (spacex_df['Payload Mass (kg)'] <= max_payload)]
    if entered_site2 == 'ALL':
        fig = px.scatter(filtered_df2, 
                         x ='Payload Mass (kg)', 
                         y ='class', 
                         title=f'Scatterplot of Relationship between Payload Mass and Launch Outcome',
                         color = 'Booster Version Category')
        return fig
    elif entered_site2 != 'ALL':
        filtered_df2 = filtered_df2[filtered_df2['Launch Site'] == entered_site2]
        fig = px.scatter(filtered_df2, 
                 x ='Payload Mass (kg)', 
                 y ='class', 
                 title=f'Scatterplot of Payload Mass and Launch Outcome from {entered_site2}', 
                 color = 'Booster Version Category')
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()