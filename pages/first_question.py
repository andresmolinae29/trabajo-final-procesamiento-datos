import dash
import dash_bootstrap_components as dbc

from dash import dcc, html, callback, Input, Output
from common import get_summary_by_program, df


dash.register_page(__name__, order=2, name="1ra. Pregunta")


table_component = dbc.Card(
    [
        dbc.CardHeader(html.H5("Tabla de cobertura por programa")),
        dbc.CardBody(
            html.Div(id='program-table-container')
        ),
    ],
)


text_component = dbc.Card(
    [
        dbc.CardHeader(html.H5("Explicación de la distribución")),
        dbc.CardBody(
            html.P(
                'Los programas más efectivos en términos de cobertura son "MI CASA YA", "Bolsa Desplazados" y "Programa Vivienda Gratuita Fase I", ya que concentran la mayor cantidad de hogares beneficiados y el mayor porcentaje de cobertura. La efectividad de estos programas puede atribuirse a su enfoque en poblaciones vulnerables y a la implementación de políticas que facilitan el acceso a la vivienda para familias de bajos ingresos.',  # noqa: E501
            ),
        ),
    ],
    className="mb-3"
)


@callback(
    Output('program-table-container', 'children'),
    Input('program-table-container', 'id')
)
def get_table(_):
    """    Callback to generate the table showing the summary of subsidies by program.
    This function retrieves the summary data and formats it into a Dash table component.
    """

    return dbc.Table.from_dataframe(
        get_summary_by_program(df),
        striped=True,
        bordered=True,
        hover=True
    )


layout = dbc.Container([
    dbc.Row([
        dbc.Col(
            html.H3("¿Cuáles son los programas de subsidios más efectivos en términos de cobertura?", style={"textAlign": "center"}),
        )
    ]),
    dbc.Row(
        dbc.Col(
            table_component,
            width=12
        ),
        style={"marginTop": "20px", "marginBottom": "20px"}
    ),
    dbc.Row(
        dbc.Col(
            text_component,
            style={"textAlign": "justify", "marginTop": "20px"}
        )
    ),
    ],
    fluid=True
)
