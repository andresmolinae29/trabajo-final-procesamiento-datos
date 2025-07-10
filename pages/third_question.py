import dash
import dash_bootstrap_components as dbc

from dash import dcc, html, callback, Input, Output
from common import get_lines_plots, df


dash.register_page(__name__, order=5, name="3ra. Pregunta")


dropdown_depts_options = [
    {"label": val, "value": val}
    for val in df["departamento"].unique()
]


dropdown_mun_options = [
    {"label": val, "value": val}
    for val in df["municipio"].unique()
]


dropdown_programs_options = [
    {"label": val, "value": val}
    for val in df["programa"].unique()
]


dropdown_depts = dcc.Dropdown(
    id="dept-dropdown",
    options=dropdown_depts_options,
    clearable=True,
    multi=True,
    placeholder="Todos los departamentos",
)


dropdown_mun = dcc.Dropdown(
    id="mun-dropdown",
    options=dropdown_mun_options,
    clearable=True,
    multi=True,
    placeholder="Todos los municipios",
)


dropdown_program = dcc.Dropdown(
    id="program-dropdown",
    options=dropdown_programs_options,
    clearable=True,
    multi=True,
    placeholder="Todos los programas",
)


graph_component = dcc.Graph(
    id='graph-container-lines',
    config={
        'displayModeBar': True,
        'modeBarButtonsToRemove': ['toImage', 'sendDataToCloud', 'editInChartStudio', 'zoom2d', 'select2d', 'lasso2d', 'autoScale2d', 'resetScale2d', 'zoomIn2d', 'zoomOut2d', 'pan2d', 'toggleHover', 'toggleSpikelines']
    },
    style={'height': '100%', 'width': '100%'}
)


text_component = dbc.Card(
    [
        dbc.CardHeader(html.H5("Explicación general:")),
        dbc.CardBody([
            html.P("El gráfico presenta la evolución del subsidio habitacional en Colombia a lo largo del tiempo. En el primer panel se observa un incremento sostenido del valor total asignado por año, con picos significativos entre 2013 y 2015, y nuevamente entre 2021 y 2023. Esto sugiere momentos de fuerte inversión pública en programas de vivienda. El segundo panel muestra la cantidad de hogares beneficiados, con una tendencia más estable pero con una caída abrupta en 2012 y una fuerte alza en 2021–2022. Finalmente, el tercer panel revela que el valor promedio asignado por hogar ha aumentado progresivamente, pasando de cifras cercanas a los 8 millones en los primeros años a más de 30 millones en promedio después de 2013, lo que indica un mayor monto de subsidio individual en años recientes. Esta evolución puede reflejar tanto ajustes por inflación como un cambio en el enfoque de los programas, priorizando montos mayores por beneficiario."
            )
        ]
        , style={'marginTop': '20px', 'marginBottom': '20px'}
            
        )
    ])


@callback(
    Output('graph-container-lines', 'figure'),
    Input('dept-dropdown', 'value'),
    Input('mun-dropdown', 'value'),
    Input('program-dropdown', 'value')
)
def update_graph_homes(selected_depts, selected_muns, selected_programs):
    """
    Updates the graph based on selected departments, municipalities, and programs.
    If no filters are applied, shows the total value assigned by department.
    """
    
    return get_lines_plots(
        df,
        depts=selected_depts if selected_depts else [],
        muns=selected_muns if selected_muns else [],
        programs=selected_programs if selected_programs else []
    )


layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H1("¿Cuáles son las tendencias de subsidios de vivienda en Colombia?", style={"textAlign": "center"}),
            ]),
            width=12
        )
    ]),
    dbc.Row([
        dbc.Col(dropdown_depts, width=4),
        dbc.Col(dropdown_mun, width=4),
        dbc.Col(dropdown_program, width=4),
    ], className="mb-4"),
    dbc.Row([
        dbc.Col(graph_component, width=12, style={'height': 'auto'}),
    ]),
    dbc.Row([
        dbc.Col(text_component, width=12, style={"marginTop": "20px", "marginBottom": "20px"})
    ])
], fluid=True, className="py-4")
