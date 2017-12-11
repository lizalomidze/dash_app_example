import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd

df = pd.read_csv(
    'DataEU.csv')
df

app = dash.Dash(__name__)
server = app.server

app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})

available_indicators = df['NA_ITEM'].unique()
available_geo = df['GEO'].unique()

app.layout = html.Div([
    # Graph 1
    html.Div([
        html.H1(children='Scatter Plot',style={'text-align':'center','font-family':'monospace'}),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='xaxis-column',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='Value added, gross'
                ),
            ],
            style={'width': '48%', 'display': 'inline-block'}),

            html.Div([
                dcc.Dropdown(
                    id='yaxis-column',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='Exports of goods'
                ),
            ],style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
        ]),

        dcc.Graph(id='indicator-graphic',
                 clickData={'points':[{'customdata':'Belgium'}]}),

        dcc.Slider(
            id='year--slider',
            min=df['TIME'].min(),
            max=df['TIME'].max(),
            value=2012,
            step=None,
            marks={str(year): str(year) for year in df['TIME'].unique()}
        )
    ]),
    # Graph 2
    html.Div([
        html.H1(children='Line Chart',style={'margin-top':'5%','text-align':'center','font-family':'monospace'}),
        html.Div([
            html.Div([
                dcc.Dropdown(
                    id='indicator-select',
                    options=[{'label': i, 'value': i} for i in available_indicators],
                    value='Final consumption expenditure and gross capital formation'
                ),
            ],
            style={'width': '48%', 'display': 'inline-block'}),

        ]),
        dcc.Graph(id='indicator-graphic2'),
    ])
    #Graph 2 End
])

@app.callback(
    dash.dependencies.Output('indicator-graphic', 'figure'),
    [dash.dependencies.Input('xaxis-column', 'value'),
     dash.dependencies.Input('yaxis-column', 'value'),
     dash.dependencies.Input('year--slider', 'value')])
def update_graph(xaxis_column_name, yaxis_column_name, year_value):
    dff = df[df['TIME'] == year_value][df['UNIT'] == "Current prices, million euro"]

    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == xaxis_column_name]['Value'],
            y=dff[dff['NA_ITEM'] == yaxis_column_name]['Value'],
            text=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            customdata=dff[dff['NA_ITEM'] == yaxis_column_name]['GEO'],
            marker={
                'size': 14,
                'color':'rgba(152, 0, 0, .8)',
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 70, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }
# Graph 2 Callback
@app.callback(
    dash.dependencies.Output('indicator-graphic2', 'figure'),
    [dash.dependencies.Input('indicator-select', 'value'),
     dash.dependencies.Input('indicator-graphic', 'clickData'),])
def update_graph(indicator_name, country_name):
    countryname = country_name['points'][0]['customdata']
    dff = df[df['GEO'] == countryname][df['UNIT'] == "Current prices, million euro"]

    return {
        'data': [go.Scatter(
            x=dff[dff['NA_ITEM'] == indicator_name]['TIME'],
            y=dff[dff['NA_ITEM'] == indicator_name]['Value'],
            text=dff[dff['NA_ITEM'] == indicator_name]['Value'],
            mode='line',
            line = dict(
                color = ('rgba(152, 0, 0, .8)'),
                width = 6,)
        )],
        'layout': go.Layout(
            xaxis={
                'title': countryname,
            },
            yaxis={
                'title': indicator_name,
            },
            margin={'l': 70, 'b': 40, 't': 10, 'r': 0},
            hovermode='closest'
        )
    }

if __name__ == '__main__':
    app.run_server()
