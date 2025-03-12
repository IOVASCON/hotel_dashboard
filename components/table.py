import dash_bootstrap_components as dbc
from dash import html

def create_table(title, df):
    """
    Cria uma tabela com título e os dados do DataFrame.
    """
    return html.Div([
        html.H3(title, className="mb-3"),
        dbc.Table.from_dataframe(
            df,
            striped=True,
            bordered=False,
            hover=True,
            responsive=True,  # Adiciona responsividade
            className="table-sm shadow"  # Adiciona sombra e tamanho pequeno
        )
    ])
