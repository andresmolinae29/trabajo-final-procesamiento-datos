import dash_bootstrap_components as dbc

from dash import Dash, html, dcc, page_registry, page_container, callback_context
from dash.dependencies import Input, Output


app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True)


def get_nav_link_style(page_path: str) -> dict:

    ctx = callback_context
    pathname = ctx.request.args.get('pathname') if ctx and hasattr(ctx, 'request') else None

    base_style = {
        "margin": "0 10px",
        "textDecoration": "none",
        "color": "#22223b",
        "fontWeight": "bold",
        "padding": "6px 16px",
        "borderRadius": "6px",
        "transition": "background 0.2s"
    }
    # If pathname matches, highlight the link
    if pathname and page_path == pathname:
        base_style.update({
            "background": "#c9ada7",
            "color": "#fff",
            "boxShadow": "0 2px 8px rgba(0,0,0,0.07)"
        })
    return base_style

app.layout = html.Div(
    [
        html.Header(
            [
                html.Div(
                    [
                        html.Img(
                            src=app.get_asset_url("logo_universidad_nacional.png"),
                            style={
                                "height": "60px",
                                "marginRight": "20px",
                                "verticalAlign": "middle"
                            }
                        ),
                        html.Div(
                            [
                                html.H1(
                                    "Trabajo Final: Procesamiento Estadístico de Datos",
                                    style={
                                        "fontSize": "2.5rem",
                                        "marginBottom": "0.2em",
                                        "color": "#22223b",
                                        "textAlign": "left"
                                    }
                                ),
                                html.H2(
                                    "Andrés Molina Escobar",
                                    style={
                                        "fontWeight": "normal",
                                        "fontSize": "1.3rem",
                                        "margin": "0",
                                        "color": "#4a4e69",
                                        "textAlign": "left"
                                    }
                                ),
                                html.H3(
                                    "CC 103764048",
                                    style={
                                        "fontWeight": "normal",
                                        "fontSize": "1rem",
                                        "margin": "0 0 1em 0",
                                        "color": "#4a4e69",
                                        "textAlign": "left"
                                    }
                                ),
                            ],
                            style={"display": "flex", "flexDirection": "column", "justifyContent": "center"}
                        )
                    ],
                    style={
                        "display": "flex",
                        "alignItems": "center",
                        "justifyContent": "center",
                        "width": "100%"
                    }
                ),
            ],
            style={"width": "100%"}
        ),
        dcc.Location(id="url"),
        html.Nav(
            id="navbar",
            style={
                "marginBottom": "1em",
                "textAlign": "center"
            }
        ),
        html.Hr(style={"width": "100%", "borderColor": "#9a8c98"}),
        html.Main(page_container, style={"width": "100%", "maxWidth": "900px"})
    ],
    style={
        "display": "flex",
        "flexDirection": "column",
        "alignItems": "center",
        "minHeight": "100vh",
        "background": "#f8f9fa",
        "paddingTop": "40px"
    }
)


@app.callback(
    Output("navbar", "children"),
    Input("url", "pathname")
)
def update_navbar(pathname):
    nav_links = []
    for page in page_registry.values():
        style = {
            "margin": "0 10px",
            "textDecoration": "none",
            "color": "#22223b",
            "fontWeight": "bold",
            "padding": "6px 16px",
            "borderRadius": "6px",
            "transition": "background 0.2s"
        }
        if pathname == page['path']:
            style.update({
                "background": "#c9ada7",
                "color": "#fff",
                "boxShadow": "0 2px 8px rgba(0,0,0,0.07)"
            })
        nav_links.append(
            dcc.Link(
                page['name'],
                href=page['path'],
                style=style
            )
        )
    return nav_links

if __name__ == '__main__':
    app.run(
        debug=False
    )