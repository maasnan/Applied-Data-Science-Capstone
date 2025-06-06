# Import required libraries
import pandas as pd
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)
MIN_PAYLOAD = 0
MAX_PAYLOAD = 10000
STEP_PAYLOAD = 1000
def get_dropdown_options(df):
    unique_sites = df['Launch Site'].unique()
    return [{'label': 'All Sites', 'value': 'ALL'}] + [{'label': site, 'value': site} for site in unique_sites]
# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),html.Div([
        dcc.Dropdown(
            id='site-dropdown',
            options=get_dropdown_options(spacex_df),
            value='ALL',
            placeholder="Select a Launch Site",
            searchable=True,
            style={'width': '50%', 'padding': '10px', 'margin': '0 auto'}
        )
    ]),

    html.Br(),

    # TASK 2: Success Pie Chart
    html.Div(dcc.Graph(id='success-pie-chart')),

    html.Br(),

    # TASK 3: Payload Range Slider
    html.Div([
        dcc.RangeSlider(
            id='payload-slider',
            min=MIN_PAYLOAD,
            max=MAX_PAYLOAD,
            step=1000,
            marks={i: f'{i} Kg' for i in range(MIN_PAYLOAD, MAX_PAYLOAD + 1000, 1000)},
            value=[spacex_df['Payload Mass (kg)'].min(), spacex_df['Payload Mass (kg)'].max()],
            tooltip={"placement": "bottom", "always_visible": True}
        )
    ], style={'width': '80%', 'padding': '0px 40px', 'margin': '0 auto'}),

    html.Br(),

    # TASK 4: Payload vs. Launch Outcome Scatter Plot
    html.Div(dcc.Graph(id='success-payload-scatter-chart'))
])

# TASK 2: Callback for Success Pie Chart
@app.callback(
    Output('success-pie-chart', 'figure'),
    Input('site-dropdown', 'value')
)
def update_pie_chart(selected_site):
    if selected_site == 'ALL':
        # Calculate overall success vs failure
        success_counts = spacex_df['class'].value_counts()
        fig = px.pie(
            names=['Failure', 'Success'],
            values=success_counts,
            title='Overall Success Rate for All Sites'
        )
    else:
        # Filter data for the selected site
        site_data = spacex_df[spacex_df['Launch Site'] == selected_site]
        site_counts = site_data['class'].value_counts()
        fig = px.pie(
            names=['Failure', 'Success'],
            values=site_counts,
            title=f'Success vs. Failure for {selected_site}'
        )

    fig.update_layout(margin=dict(t=50, b=0, l=0, r=0))
    return fig

# TASK 4: Callback for Scatter Plot
@app.callback(
    Output('success-payload-scatter-chart', 'figure'),
    Input('site-dropdown', 'value'),
    Input('payload-slider', 'value')
)
def update_scatter_plot(selected_site, payload_range):
    low, high = payload_range

    # Filter data based on payload range
    filtered_df = spacex_df[(spacex_df['Payload Mass (kg)'] >= low) & (spacex_df['Payload Mass (kg)'] <= high)]

    # Filter for specific site if selected
    if selected_site != 'ALL':
        filtered_df = filtered_df[filtered_df['Launch Site'] == selected_site]

    # Create scatter plot
    fig = px.scatter(
        filtered_df,
        x='Payload Mass (kg)',
        y='class',
        color='Booster Version Category',
        title=f'Payload vs. Launch Outcome for {"All Sites" if selected_site == "ALL" else selected_site}',
        labels={'class': 'Launch Outcome', 'Payload Mass (kg)': 'Payload Mass (kg)'},
        hover_data=['Launch Site']
    )

    fig.update_layout(
        yaxis=dict(tickvals=[0, 1], ticktext=['Failure', 'Success']),
        plot_bgcolor='rgba(0, 0, 0, 0)',
        margin=dict(t=50, b=0, l=0, r=0)
    )

    return fig

                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                # dcc.Dropdown(id='site-dropdown',...)
                               

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                


                                # TASK 3: Add a slider to select payload range
                                #dcc.RangeSlider(id='payload-slider',...)

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success


# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output


# Run the app
if __name__ == '__main__':
    app.run()
