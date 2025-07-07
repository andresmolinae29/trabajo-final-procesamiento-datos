import json
import pandas as pd
import os

from functools import cache
from definitions import FILE_NAME, ROOT_DIR


def load_json(file_name: str) -> dict:
    """Load a JSON file and return its content as a dictionary."""

    file_path = os.path.join(ROOT_DIR, 'assets', file_name)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"JSON file {file_path} not found")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)


def clean_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """Clean column names by removing spaces and converting to lowercase."""
    df.columns = df.columns.str.replace(' ', '_').str.lower()
    df.columns = df.columns.str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
    return df


@cache
def load_data() -> pd.DataFrame:

    data_path = os.path.join(ROOT_DIR, 'data', FILE_NAME)

    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file {FILE_NAME} not found in {data_path}")
    
    df = pd.read_csv(data_path, encoding='utf-8')
    df = clean_column_names(df)

    df = df.loc[df['estado_de_postulacion'] == 'Asignados']

    df = df.groupby(['ano_de_asignacion', 'departamento', 'municipio', 'programa', 'estado_de_postulacion'], as_index=False).agg({
        'valor_asignado': 'sum',
        'hogares': 'sum'
    })

    df['valor_por_hogar'] = df['valor_asignado'] / df['hogares']

    return df


df = load_data()