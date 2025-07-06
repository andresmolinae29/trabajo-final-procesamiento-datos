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
            html.P(
                "Esta visualización muestra la evolución general —sin filtros por región, programa ni población— del subsidio familiar de vivienda administrado por FONVIVIENDA desde 2003 hasta 2025, analizada en tres dimensiones: valor total asignado, hogares beneficiados y valor promedio por hogar."),
            html.P(
                "En el primer gráfico, se observa un incremento notable en el valor asignado por año, con un salto abrupto en 2012 y picos importantes alrededor de 2014, 2021 y 2022, donde se superaron los 2 billones de pesos anuales. Este comportamiento refleja decisiones presupuestales estratégicas y posiblemente la implementación de programas de alto impacto como Mi Casa Ya. Hacia 2025, el valor cae bruscamente, lo cual puede deberse a rezagos en ejecución, cierre de programas o corte de la actualización."
            ),
            html.P(
                "El segundo gráfico muestra el número de hogares beneficiados por año, con una tendencia más variable. Se destacan aumentos en 2007 y especialmente entre 2021 y 2022, con más de 80.000 hogares beneficiados anualmente, seguidos por una caída en 2025. Esta variabilidad sugiere que la cantidad de subsidios entregados no siempre crece proporcionalmente con el presupuesto.",
            ),
            html.P(
                "El tercer gráfico, que muestra el valor promedio asignado por hogar, permite identificar cambios estructurales: desde valores cercanos a los 7 millones en 2003, se alcanza un pico de más de 35 millones por hogar en 2013. Posteriormente, aunque el valor promedio se mantiene elevado, oscila entre 22 y 30 millones hasta 2025. Esto indica una evolución en la política de subsidios, posiblemente hacia un mayor monto unitario por hogar."
            ),
            html.P(
                "En conjunto, los gráficos reflejan una tendencia general hacia la ampliación y fortalecimiento de la inversión pública en vivienda, aunque con comportamientos dispares año a año, posiblemente influenciados por factores económicos, políticos o emergencias sociales."
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
