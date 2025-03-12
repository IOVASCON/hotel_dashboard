import dash_bootstrap_components as dbc
from dash import html

def create_progress_list(items):
    """
    Cria uma lista de barras de progresso.
    """
    return html.Div([
        html.H3("Metas", className="mb-3"),
        *[dbc.Progress(
            value=item["value"],
            color=item["color"],
            label=f'{item["label"]}: {item["value"]}%',
            className="mb-3 shadow"  # Adiciona sombra
        ) for item in items]
    ])
