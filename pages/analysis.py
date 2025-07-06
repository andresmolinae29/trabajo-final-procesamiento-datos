import dash
import dash_bootstrap_components as dbc

from dash import dcc, html, callback, Input, Output
from common import (
    df,
    get_summary_statistics,
    graph_variable,
    load_json
)


dash.register_page(__name__, order=1, name="Análisis de datos")


dropdown_options = [
    {"label": "Departamento", "value": "departamento"},
    {"label": "Municipio", "value": "municipio"},
    {"label": "Programa", "value": "programa"},
    {"label": "Estado de postulación", "value": "estado_de_postulacion"},
    {"label": "Hogares", "value": "hogares"},
    {"label": "Valor asignado", "value": "valor_asignado"},
    {"label": "Valor por hogar", "value": "valor_por_hogar"},
]


explanation_text = load_json('distributions_explanation.json')


# Ensure the graph fills its card and is vertically centered
dropdown_component = dbc.InputGroup(
    [
        dcc.Dropdown(
            options=dropdown_options,
            value='departamento',  # Default value
            id='dropdown',
            multi=False,
            clearable=False,
            style={"minWidth": "200px"}
        ),
    ],
    className="mb-2"
)


table_component = dbc.Card(
    [
        dbc.CardHeader(html.H5("Resumen de estadísticas")),
        dbc.CardBody(
            html.Div(id='dd-output-container')
        ),
    ],
    className="mb-3"
)


graph_component = dbc.Card(
    [
        dbc.CardHeader(html.H5("Gráficos")),
        dbc.CardBody(
            html.Div(
                dcc.Graph(id='graph-container', style={'height': '100%', 'width': '100%'}),
                style={'display': 'flex', 'alignItems': 'center'}
            )
        ),
    ],
    className="mb-3 h-100"
)


text_component = dbc.Card(
    [
        dbc.CardHeader(html.H5("Explicación de la distribución")),
        dbc.CardBody(
            html.Div(id='text-explanation', style={'marginTop': '20px'})
        ),
    ],
    className="mb-3"
)


@callback(
    Output('dd-output-container', 'children'),
    Input('dropdown', 'value')
)
def build_table(selected_value: str):
    """ Builds a summary statistics table based on the selected variable from the dropdown.
    """
    summary_df = get_summary_statistics(df, selected_value)
    return dbc.Table.from_dataframe(summary_df, striped=True, bordered=True, hover=True)


@callback(
    Output('graph-container', 'figure'),
    Input('dropdown', 'value')
)
def build_graph(selected_value: str):
    """ Builds a graph based on the selected variable from the dropdown.
    """
    selected_label = next((opt["label"] for opt in dropdown_options if opt["value"] == selected_value), selected_value)
    return graph_variable(df, selected_value, selected_label)


@callback(
    Output('text-explanation', 'children'),
    Input('dropdown', 'value')
)
def get_text_explanation(selected_value: str):
    """
    Returns an explanation text based on the selected variable.
    """
    return explanation_text.get(selected_value, "No hay explicación disponible para esta variable.")


layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.H3("Análisis de Datos", className="mb-4"),
            width=12
        )
    ]),
    dbc.Row([
        dbc.Col(
            html.P("Seleccione una variable para analizar:"),
            width=12
        )
    ]),
    dbc.Row([
        dbc.Col(dropdown_component, width=4),
    ], className="mb-3"),
    dbc.Row([
        dbc.Col(table_component, width=5),
        dbc.Col(graph_component, width=7, style={'height': 'auto'}),
    ], className="g-4"),
    dbc.Row([
        dbc.Col(text_component, width=12, style={"marginTop": "20px", "marginBottom": "20px"})
    ])
], fluid=True, className="py-4")