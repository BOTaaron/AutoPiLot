import dash
from dash import dcc
from dash import html
import plotly.graph_objs as go
from dash.dependencies import Input, Output
import requests
import collections

app = dash.Dash(__name__, requests_pathname_prefix='/dashapp/', routes_pathname_prefix='/dashapp/')

altitude_data = collections.deque(maxlen=80)
pressure_data = collections.deque(maxlen=80)

app.layout = html.Div([
    html.Div([
        dcc.Graph(id='altitude-chart', style={'height': '30vh'}),
        dcc.Graph(id='pressure-chart', style={'height': '30vh'})
    ], className='dash-graph-container'),
    html.Div([
        dcc.Graph(id='motor-output-gauge', style={'height': '30vh', 'width': '50%', 'display': 'inline-block'}),
        dcc.Graph(id='temperature-gauge', style={'height': '30vh', 'width': '50%', 'display': 'inline-block'})
    ], className='dash-gauge-container'),
    dcc.Interval(
        id='interval-component',
        interval=2*1000,  # Update every 2 seconds
        n_intervals=0
    )
])

# Function to fetch data from the Flask app
def fetch_data(endpoint):
    response = requests.get(f'http://localhost:5000/data/{endpoint}')
    return response.json()


@app.callback(
    Output('altitude-chart', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_altitude_chart(n):
    data = fetch_data('barometric')
    altitude_data.append(data.get('altitude', 0))
    x_values = list(range(len(altitude_data)))
    y_values = list(altitude_data)
    figure = {
        'data': [
            go.Scatter(x=x_values, y=y_values, mode='lines+markers', name='Altitude'),
            go.Scatter(x=[x_values[-1]], y=[y_values[-1]], mode='markers+text', name='Most Recent', text=[f'{y_values[-1]:.2f}'], textposition='top right')
        ],
        'layout': go.Layout(
            title='Altitude',
            yaxis=dict(range=[50, 250]),
            paper_bgcolor='#2e2e2e',
            plot_bgcolor='#2e2e2e',
            font=dict(color='#e0e0e0')
        )
    }
    return figure


@app.callback(
    Output('motor-output-gauge', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_motor_output_gauge(n):
    data = fetch_data('motor_output').get('motor_output', 0)
    figure = {
        'data': [
            go.Indicator(
                mode="gauge+number",
                value=data,
                title={'text': "Motor Output"},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkblue"},
                    'steps': [
                        {'range': [0, 50], 'color': "lightgray"},
                        {'range': [50, 75], 'color': "gray"},
                        {'range': [75, 100], 'color': "darkgray"}
                    ],
                }
            )
        ],
        'layout': go.Layout(
            title='Motor Output',
            paper_bgcolor='#2e2e2e',
            plot_bgcolor='#2e2e2e',
            font=dict(color='#e0e0e0')
        )
    }
    return figure



@app.callback(
    Output('temperature-gauge', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_temperature_gauge(n):
    data = fetch_data('barometric').get('temperature', 0)
    figure = {
        'data': [
            go.Indicator(
                mode="gauge+number",
                value=data,
                title={'text': "Temperature"},
                number={'valueformat': '.1f'},
                gauge={
                    'axis': {'range': [None, 100]},
                    'bar': {'color': "darkred"},
                    'steps': [
                        {'range': [0, 60], 'color': "lightyellow"},
                        {'range': [60, 75], 'color': "orange"},
                        {'range': [75, 100], 'color': "red"}
                    ],
                }
            )
        ],
        'layout': go.Layout(
            title='Temperature',
            paper_bgcolor='#2e2e2e',
            plot_bgcolor='#2e2e2e',
            font=dict(color='#e0e0e0')
        )
    }
    return figure


@app.callback(
    Output('pressure-chart', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_pressure_chart(n):
    data = fetch_data('barometric')
    pressure_data.append(data.get('pressure', 0))
    x_values = list(range(len(pressure_data)))
    y_values = list(pressure_data)
    figure = {
        'data': [
            go.Scatter(x=x_values, y=y_values, mode='lines+markers', name='Pressure'),
            go.Scatter(x=[x_values[-1]], y=[y_values[-1]], mode='markers+text', name='Most Recent', text=[f'{y_values[-1]:.2f}'], textposition='top right')
        ],
        'layout': go.Layout(
            title='Pressure',
            yaxis=dict(range=[950, 1050]),
            paper_bgcolor='#2e2e2e',
            plot_bgcolor='#2e2e2e',
            font=dict(color='#e0e0e0')
        )
    }
    return figure



