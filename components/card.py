import dash_bootstrap_components as dbc
from dash import html

def create_card(title, value, color="primary", icon=None):
    """
    Cria um card com título, valor e, opcionalmente, um ícone.
    """
    card_body_children = []

    # Adiciona o ícone se fornecido
    if icon:
        card_body_children.append(html.I(className=f'{icon} me-2 fa-lg', style={'color': 'white'}))

    # Adiciona o título e o valor
    card_body_children.extend([
        html.H5(title, className="card-title text-white"),  # Título menor
        html.H3(value, className="card-text text-white", style={'textAlign': 'right', 'marginLeft': '10px'})  # Valor menor e alinhado à direita
    ])

    return dbc.Card(
        dbc.CardBody(card_body_children, className="d-flex align-items-center"),  # Alinha verticalmente
        color=color,
        inverse=True,
        className="shadow h-100"  # Adiciona sombra e ocupa todo o espaço vertical
    )
