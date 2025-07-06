import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

from plotly.subplots import make_subplots
from plotly.graph_objects import Figure


def get_data_type(df: pd.DataFrame, variable: str) -> str:
    """
    Returns the data type of the specified variable.
    """
    return df[variable].dtype.name


def get_summary_statistics(df: pd.DataFrame, variable: str) -> pd.DataFrame:
    """
    Returns summary statistics for the specified variable.
    """
    
    data_type = get_data_type(df, variable)
    if data_type in ['int64', 'float64']:
        return df[variable].describe().reset_index().rename(columns={'index': 'Estadístico', variable: 'Valor'})
    elif data_type == 'object':
        return df.groupby(
            variable, as_index=False
            )['hogares'].agg(['sum']).rename(
                columns={'sum': 'Total Hogares'}
                ).sort_values(
                    by='Total Hogares', ascending=False
                    ).head(10)
    else:
        raise ValueError(f"Unsupported data type: {data_type}")


def graph_variable(df: pd.DataFrame, variable: str, variable_name: str = None) -> Figure:
    """
    Returns an improved Plotly figure for the specified variable.
    For numerical variables: shows both histogram and boxplot.
    For categorical variables: shows a sorted horizontal bar chart of top 10 categories.
    """
    data_type = get_data_type(df, variable)
    
    if data_type in ['int64', 'float64']:

        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            row_heights=[0.7, 0.3],
                            vertical_spacing=0.05,
                            subplot_titles=(f"Histograma de {variable_name}", f"Boxplot de {variable_name}"))

        # Calculate an appropriate number of bins using the Freedman-Diaconis rule
        data = df[variable].dropna()
        q25, q75 = data.quantile([0.25, 0.75])
        iqr = q75 - q25
        bin_width = 2 * iqr / (len(data) ** (1/3)) if iqr > 0 else None
        if bin_width and bin_width > 0:
            bins = int((data.max() - data.min()) / bin_width)
            bins = max(1, bins)
        else:
            bins = 30  # fallback

        if bins > 30:
            bins = 30
            data = np.log10(data + 1)  # Log transform if too many bins
            title_suffix = " (Log Transformado)"
        else:
            title_suffix = ""

        fig.add_trace(
            go.Histogram(x=data, name='Histograma', marker_color='skyblue', nbinsx=bins),
            row=1, col=1
        )
        fig.add_trace(
            go.Box(x=data, name='Boxplot', marker_color='orange', boxmean='sd', orientation='h'),
            row=2, col=1
        )
        fig.update_layout(height=600, showlegend=False)
        fig.update_xaxes(title_text=f"{title_suffix} {variable}", row=2, col=1)
        fig.update_yaxes(title_text="Frecuencia", row=1, col=1)

    elif data_type == 'object':

        value_counts = df.groupby([variable], as_index=False)['hogares'].agg(['sum']).rename(columns={'sum': 'Total Hogares'})
        value_counts = value_counts.sort_values(by='Total Hogares', ascending=False).head(10)
        fig = px.bar(
            value_counts,
            x='Total Hogares', y=variable,
            orientation='h',
            title=f"Top 10 categorías de {variable_name}",
            labels={variable: 'Frecuencia'}
        )
        fig.update_layout(yaxis={'categoryorder':'total ascending'})
    else:
        raise ValueError(f"Unsupported data type: {data_type}")
    
    return fig


def get_lines_plots(df: pd.DataFrame, depts: list[str], muns: list[str], programs: list[str]) -> Figure:
    """
    Returns a Plotly figure with multiple line plots for the specified departments, municipalities, and programs.
    """
    filtered_df = df.copy()

    if depts:
        filtered_df = filtered_df[filtered_df['departamento'].isin(depts)]
    
    if muns:
        filtered_df = filtered_df[filtered_df['municipio'].isin(muns)]
    
    if programs:
        filtered_df = filtered_df[filtered_df['programa'].isin(programs)]

    filtered_df = filtered_df.groupby(
        ['ano_de_asignacion'],
        as_index=False
    ).agg({
        'hogares': 'sum',
        'valor_asignado': 'sum',
        'valor_por_hogar': 'mean'
    })

    filtered_df = filtered_df.sort_values(by='ano_de_asignacion')

    fig = make_subplots(
        rows=3, 
        cols=1, 
        subplot_titles=(
            "Valor Asignado por Año",
            "Hogares Beneficiados por Año",
            "Valor por Hogar Promedio por Año"
        ),
        row_heights=[2, 2, 2],
        vertical_spacing=0.1
    )

    fig.add_trace(
        go.Scatter(x=filtered_df['ano_de_asignacion'], y=filtered_df['valor_asignado'], mode='lines+markers', name='Valor Asignado'),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=filtered_df['ano_de_asignacion'], y=filtered_df['hogares'], mode='lines+markers', name='Hogares Beneficiados'),
        row=2, col=1
    )
    
    fig.add_trace(
        go.Scatter(x=filtered_df['ano_de_asignacion'], y=filtered_df['valor_por_hogar'], mode='lines+markers', name='Valor por Hogar Promedio'),
        row=3, col=1
    )

    fig.update_layout(height=600, showlegend=False)
    
    return fig


def top_5_regions(df: pd.DataFrame, variable: str) -> pd.DataFrame:
    """
    Returns a DataFrame with the top 5 regions based on the specified variable.
    """
    if variable not in df.columns:
        raise ValueError(f"Variable '{variable}' not found in DataFrame.")
    
    if variable == 'valor_por_hogar':
        summarization_value = 'mean'
    else:
        summarization_value = 'sum'
    
    top_regions = df.groupby(['departamento'], as_index=False)[variable].agg([summarization_value]).sort_values(
        by=summarization_value, ascending=False
    ).head(5)

    df_top_regions = df[df['departamento'].isin(top_regions['departamento'].unique())]

    return df_top_regions


def box_plots(df: pd.DataFrame, summarization_value: str) -> Figure:

    if summarization_value not in ['valor_asignado', 'hogares', 'valor_por_hogar']:
        raise ValueError("summarization_value must be one of 'valor_asignado', 'hogares', or 'valor_por_hogar'.")

    departments = df['departamento'].unique()
    departments = sorted(departments)[:5]

    fig = go.Figure()

    for dept in departments:
        dept_data = df[df['departamento'] == dept][summarization_value]
        log_normal = False
        if summarization_value != 'valor_por_hogar':
            dept_data = np.log(dept_data.replace(0, np.nan)).dropna()
            log_normal = True
        fig.add_trace(
            go.Box(
                y=dept_data,
                name=str(dept),
                boxmean='sd'
            )
        )

    fig.update_layout(
        title=f"Distribución de {'Log normal ' if log_normal else ''}{summarization_value.replace('_', ' ').title()} por Departamento",
        xaxis_title="Departamento",
        height=500
    )

    return fig

    
def get_summary_by_program(df: pd.DataFrame) -> pd.DataFrame:
    """
    Returns a DataFrame summarizing the number of households and total assigned value by program.
    """
    program_coverage = df.groupby(['programa'], as_index=False).agg(
        hogares=('hogares', 'sum')
    )

    total_hogares = program_coverage['hogares'].sum()
    program_coverage['porcentaje'] = round((program_coverage['hogares'] / total_hogares) * 100, 2)

    return program_coverage.sort_values(by='hogares', ascending=False)
