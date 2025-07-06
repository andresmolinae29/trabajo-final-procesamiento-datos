import dash
import dash_bootstrap_components as dbc

from dash import dcc, html, callback, Input, Output
from common import df, top_5_regions, box_plots, load_json


dash.register_page(__name__, order=3, name="2da. Pregunta")


dropdown_options = [
    {"label": "Hogares", "value": "hogares"},
    {"label": "Valor asignado", "value": "valor_asignado"},
    {"label": "Valor por hogar", "value": "valor_por_hogar"},
]


explanation_text = load_json('distribution_region_explanation.json')


dropdown_component = dbc.InputGroup(
    [
        dcc.Dropdown(
            options=dropdown_options,
            value='hogares',  # Default value
            id='dropdown_regions',
            multi=False,
            clearable=False,
            style={"minWidth": "200px"}
        ),
    ],
    className="mb-2"
)


graph_component = dcc.Graph(
    id='graph-container-regions',
    config={
        'displayModeBar': True,
        'modeBarButtonsToRemove': ['toImage', 'sendDataToCloud', 'editInChartStudio', 'zoom2d', 'select2d', 'lasso2d', 'autoScale2d', 'resetScale2d', 'zoomIn2d', 'zoomOut2d', 'pan2d', 'toggleHover', 'toggleSpikelines']
    },
    style={'height': '100%', 'width': '100%'}
)


text_component = dbc.Card(
    [
        dbc.CardHeader(html.H5("Explicación de la distribución por región")),
        dbc.CardBody(
            html.Div(id='region-explanation', style={"textAlign": "justify"}),
            style={"marginTop": "20px", "marginBottom": "20px"}
        ),
    ],
    className="mb-3"
)


@callback(
    Output('graph-container-regions', 'figure'),
    Input('dropdown_regions', 'value')
)
def build_graph(selected_value: str):
    """ Builds a graph showing the distribution of housing subsidies by region.
    """
    df_filtered = df.loc[df['programa'] == 'MI CASA YA']
    top_regions = top_5_regions(df_filtered, selected_value)

    return box_plots(top_regions, selected_value)


@callback(
    Output('region-explanation', 'children'),
    Input('dropdown_regions', 'value')
)
def update_explanation(selected_value: str):
    """ Updates the explanation text based on the selected variable.
    """
    return explanation_text.get(selected_value, "No hay explicación disponible para esta variable.")


layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H1("¿Cómo se distribuye el subsidio mi casa ya por región?", style={"textAlign": "center"}),
            ])
        )
    ]),
    dbc.Row([
        dbc.Col(html.P("Seleccione una variable para visualizar su distribución por región:"), className="d-flex align-items-center justify-content-end"),
        dbc.Col(dropdown_component, width=4, className="d-flex align-items-center justify-content-center"),
    ], style={"marginTop": "5px", "marginBottom": "20px"}),
    dbc.Row([
        dbc.Col(graph_component, width=12, style={'height': 'auto'}),
    ]),
    dbc.Row([
        dbc.Col(text_component, width=12, style={"marginTop": "20px", "marginBottom": "20px"})
    ]),
], fluid=True,)