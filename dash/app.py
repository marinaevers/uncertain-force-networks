from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import callbacks
import visualizations
import dash_daq as daq
import sankey_tracking_graph
import uncertain_graph_view
import dash_auth

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])#, requests_pathname_prefix='/dash/')

VALID_USERNAME_PASSWORD_PAIRS = {
    'e1': 'granular',
    'e2': 'material',
    'test': 'uncertain',
    'notrack': 'notrack'  # Added 'notrack' user for no tracking
}

auth = dash_auth.BasicAuth(
    app,
    VALID_USERNAME_PASSWORD_PAIRS,
    secret_key='this-is-a-secret-key'
)

app.layout = html.Div(
    [
        dbc.Row( # Other views
        [
            dbc.Col([ # Spatial view
                html.Div(id='spatial', style={}, children=[
                    uncertain_graph_view.UncertainGraphView(
                    id='spatial-diagram',
                    positions=[[[]]],
                    radii=[[]],
                    ccs=[[[]]],
                    edges=[[]],
                    showEdges=None,
                    orderByColorSimilarity=None,
                    useSizeForProbabilities=None,
                    colormap=None,
                    saveOnClick=False,
                    #clickData=None  # Initialize as None, will be updated by click events
                )
            ]),
            ], xs=12, sm=12, md=12, lg=4, xl=4),
            dbc.Col([ # Settings Spatial view
                daq.ToggleSwitch(
                    label='Show edges',
                    labelPosition='top',
                    id='show-edges',
                ),
                daq.ToggleSwitch(
                    label='Order by color similarity',
                    labelPosition='top',
                    id='order-color',
                ),
                daq.ToggleSwitch(
                    label='Use size for probability',
                    labelPosition='top',
                    id='use-size',
                ),
                                daq.ToggleSwitch(
                    label='Show major/minor',
                    labelPosition='top',
                    id='show-major-minor',
                ),
                daq.ToggleSwitch(
                    label='User-defined threshold',
                    labelPosition='top',
                    id='user-defined-threshold',
                    style={'display': 'none'}
                ),
                daq.ToggleSwitch(
                    label='Aggregate jammed',
                    labelPosition='top',
                    id='aggregate-jammed',
                    style={'display': 'none'}
                ),
                html.Div("Avg. force: 0.0", id='avg-force-text', style={'marginTop': '10px'}),
            ], xs=12, sm=12, md=6, lg=2, xl=2),
            dbc.Col([ # Graph measures
                visualizations.createGraphMeasureView('avg-degree'),
                visualizations.createGraphMeasureView('cc-size'),
                visualizations.createGraphMeasureView('nonparticipating'),
            ], xs=12, sm=12, md=6, lg=6, xl=6),
        ], className='mb-3'),
         dbc.Row( # Sankey
        [
            # html.H1("Sankey Diagram", style={'height': '25vh'}),
            html.Div(id='sankey', children=[
                sankey_tracking_graph.SankeyTrackingGraph(
                    id='sankey-diagram',
                    links=None,
                    colorPositions=None,
                    height=600,
                    colormap=None,
                    step = 0,
                    nodeMap=None
                )
            ], style={})
        ], className='mb-3'),
        dbc.Row( # Settings
        [
            html.Details([
                html.Summary('Settings'),
                dbc.Row([
                    dbc.Col([
                        dcc.Upload(
                            id='upload-data',
                            children=html.Div([
                                'Drag and Drop or Select Data File (.json)'
                            ]),
                            style={
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px 0'
                            },
                            # Allow multiple files to be uploaded
                            multiple=True
                        )
                    ], xs=12, sm=12, md=4, lg=4, xl=4),
                    dbc.Col([
                        dcc.Upload(
                            id='upload-state',
                            children=html.Div([
                                'Drag and Drop or Select State File (.json)'
                            ]),
                            style={
                                'height': '60px',
                                'lineHeight': '60px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                'textAlign': 'center',
                                'margin': '10px 0',
                            },
                            # Allow multiple files to be uploaded
                            multiple=False
                        )
                    ], xs=12, sm=12, md=4, lg=4, xl=4),
                    dbc.Col([
                        dbc.Button('Save State', id='save-state', style={
                            'height': '60px',
                            'width': '100%',
                            'margin': '10px 0'
                        })
                    ], xs=12, sm=12, md=4, lg=4, xl=4)
                ]),
                dbc.Row([
                    dbc.Col([
                        dcc.Dropdown(['BREMM', 'CUBEDIAGONAL', 'SCHUMANN', 'STEIGER', 'TEULINGFIG2', 'ZIEGLER'], 'ZIEGLER', id='select-colormap'),
                    ], width=12)
                ], className='mb-2'),
                dbc.Row([
                    dbc.Col([
                        daq.ToggleSwitch(
                            label='Save on click',
                            labelPosition='bottom',
                            id='save-on-click',
                            value=True
                        )
                    ], width=12)
                ]),
            ])
        ]),
        dcc.Store(id='store-data'),
        dcc.Store(id='spatial-data'),
        dcc.Store(id='thresholded-forces-data'),
        dcc.Store(id='step-data')
    ], className='container-fluid p-3'
)

server = app.server
if __name__ == '__main__':
    #print(callbacks.compute_connected_components.cache_info())
    app.run(debug=False)
    #pass