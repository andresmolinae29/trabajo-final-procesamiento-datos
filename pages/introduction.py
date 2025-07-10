import dash

from dash import dcc, html
from common import df


dash.register_page(__name__, order=0, name="Introducción")


layout = html.Div([
       html.P(
              "Este proyecto realiza un análisis exploratorio de datos sobre subsidios de vivienda en Colombia, "
              "utilizando Dash y Plotly para la visualización interactiva. El objetivo principal es comprender la evolución, "
              "distribución y características de los subsidios otorgados en el país."
       ),
       html.A(
              "GitHub",
              href="https://github.com/andresmolinae29/trabajo-final-procesamiento-datos",
              target="_blank",
              style={
                     "color": "#000000",
                     "fontWeight": "bold"
              }
       ),
       html.Br(),
       html.Br(),
       html.P(
              "A lo largo del análisis, se examinarán tendencias temporales, distribución geográfica y tipos de subsidios, "
              "apoyados en gráficos dinámicos que facilitan la interpretación de los datos."
       ),
       html.P(
              "La información utilizada proviene de fuentes oficiales, ha sido depurada y transformada para garantizar su calidad y utilidad en el análisis."
       ),
       html.A(
              "Descargar los datos utilizados",
              href="https://www.datos.gov.co/Vivienda-Ciudad-y-Territorio/Subsidios-De-Vivienda-Asignados/h2yr-zfb2/about_data",
              target="_blank",
              style={
                     "color": "#000000",
                     "fontWeight": "bold"
              }
       ),
       html.Br(),
       html.Br(),
       html.P(
              "El archivo de datos contiene el número de hogares beneficiarios del subsidio familiar de vivienda otorgado por el Fondo Nacional de Vivienda (FONVIVIENDA), "
              "incluyendo información desde 2003 hasta la fecha de actualización (20250702), clasificada por departamento, municipio, programa y otras variables relevantes."
              "(Para el estudio solo se tuvo en cuenta los datos como estado de postulación igual a: Asignados)."
       ),
       html.P("En este análisis se abordarán las siguientes preguntas:"),
       html.Ul([
              html.Li("¿Cuáles son las tendencias históricas de los subsidios de vivienda en Colombia?"),
              html.Li("¿Cómo se distribuyen los subsidios por región y tipo?"),
              html.Li("¿Cuáles son los programas de subsidios más efectivos en términos de cobertura?"),
       ]),
       html.Hr(),
       html.H3("Resumen de la base de datos:", style={"marginTop": "30px"}),
       html.P(f"La base de datos contiene {df.shape[0]} filas y {df.shape[1]} columnas."),
       dcc.Loading(
              html.Div(
                     id="df-info-table",
                     children=[
                            html.Table(
                                   # Build table header
                                   [html.Tr([
                                          html.Th("Columna", style={"backgroundColor": "#c9ada7", "color": "white"}),
                                          html.Th("Tipo", style={"backgroundColor": "#c9ada7", "color": "white"}),
                                          html.Th("Valores no nulos", style={"backgroundColor": "#c9ada7", "color": "white"}),
                                          html.Th("Valores únicos", style={"backgroundColor": "#c9ada7", "color": "white"}),
                                   ])] +
                                   # Build table rows
                                   [
                                          html.Tr([
                                                 html.Td(col, style={"padding": "6px"}),
                                                 html.Td(str(dtype), style={"padding": "6px"}),
                                                 html.Td(str(non_null), style={"padding": "6px"}),
                                                 html.Td(str(unique), style={"padding": "6px"}),
                                          ], style={"backgroundColor": "#f9f9f9" if i % 2 == 0 else "#e0e7ef"})
                                          for i, (col, dtype, non_null, unique) in enumerate(
                                                 zip(
                                                        df.columns,
                                                        df.dtypes,
                                                        df.notnull().sum(),
                                                        df.nunique()
                                                 )
                                          )
                                   ],
                                   style={
                                          "width": "100%",
                                          "borderCollapse": "collapse",
                                          "marginTop": "10px",
                                          "fontSize": "15px",
                                          "boxShadow": "0 2px 8px rgba(0,0,0,0.05)",
                                          "border-collapse": "separate",
                                          "border": "solid black 1px",
                                          "border-radius": "6px"
                                   }
                            )
                     ],
                     style={"overflowX": "auto", "marginBottom": "30px"}
              ),
              type="circle"
       )
])