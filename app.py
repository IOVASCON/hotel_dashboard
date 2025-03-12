import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import dash_bootstrap_components as dbc
from babel.numbers import format_currency

# Módulos auxiliares
from components import card, table, progress_list
from utils import helpers
from data_processing import process_data
from visualizations import charts

# ------------------------------------------------
# CONFIGURAÇÕES
# ------------------------------------------------

DATA_FILE = "data/hotel_luxo_jan2000_dez2024.csv"

MENU_ITEMS = [
    {"label": "Visão Geral", "href": "/"},
    {"label": "Desempenho de Reservas", "href": "/desempenho-reservas"},
    {"label": "Análise de Tarifas", "href": "/analise-tarifas"},
    {"label": "Previsão de Demanda", "href": "/previsao-demanda"},
    {"label": "Gestão de Ofertas", "href": "/gestao-ofertas"},
    {"label": "Relatórios Financeiros", "href": "/relatorios-financeiros"},
    {"label": "Indicadores de Satisfação", "href": "/satisfacao"},
    {"label": "Configurações", "href": "/configuracoes"},
]

def load_data():
    """
    Carrega o DataFrame do arquivo CSV e processa; se falhar, encerra.
    """
    df = process_data.load_and_process_data(DATA_FILE)
    if df is None:
        print("Erro ao carregar os dados. O aplicativo não pode continuar.")
        exit()
    return df

def calculate_metrics(df):
    """
    Calcula métricas (Ocupacao, ADR, RevPAR etc.) e as adiciona ao DataFrame.
    """
    try:
        df['Ocupacao'] = helpers.calcular_ocupacao(df['quartos_ocupados_dia'], df['total_quartos'])
        df['ADR'] = helpers.calcular_adr(df['receita_quartos_dia'], df['quartos_ocupados_dia'])
        df['RevPAR'] = helpers.calcular_revpar(df['ADR'], df['Ocupacao'])
        df['TRevPAR'] = helpers.calcular_trevpar(df['receita_total_dia'], df['total_quartos'])
        df['GOP'] = df['lucro_operacional_bruto_dia']
        df['GOPPAR'] = df['goppar_dia']
        return df
    except Exception as e:
        print(f"Erro ao calcular as métricas: {e}")
        exit()

def prepare_table_data(df):
    """
    Retorna apenas 5 reservas recentes (nome_cliente, data, tipo_de_quarto, valor_total_diarias).
    Converte datas e formata valores para BRL.
    """
    data_tabela = df[['nome_cliente', 'data', 'tipo_de_quarto', 'valor_total_diarias']].copy()
    data_tabela['data'] = pd.to_datetime(data_tabela['data'])
    data_tabela = data_tabela.sort_values(by='data', ascending=False)
    data_tabela['data'] = data_tabela['data'].dt.strftime('%d/%m/%Y')
    data_tabela['valor_total_diarias'] = data_tabela['valor_total_diarias'].apply(
        lambda x: format_currency(x, 'BRL', locale='pt_BR')
    )
    return data_tabela.head(5)

def prepare_donut_chart_data(df):
    """
    Prepara dados para um gráfico de rosca, contando 'tipo_de_quarto'.
    """
    data_rosca = df['tipo_de_quarto'].value_counts().reset_index()
    data_rosca.columns = ['Tipo', 'Quantidade']
    return data_rosca

df = load_data()
df = calculate_metrics(df)

def format_date_br(date_str):
    """
    Converte data ISO (YYYY-MM-DD) para DD/MM/YYYY. Se None, retorna 'Nenhuma'.
    """
    if date_str:
        try:
            d = pd.to_datetime(date_str)
            return d.strftime('%d/%m/%Y')
        except:
            return 'Formato Inválido'
    return 'Nenhuma'

def create_sidebar():
    """
    Cria o menu lateral (sidebar) fixo à esquerda,
    com altura total da tela (100vh) e um padding básico.
    """
    sidebar = html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('logo.webp'),
                     style={'width': '80%', 'margin': '10px auto', 'display': 'block'}),
            html.Hr(style={'borderColor': '#fff'})
        ], style={'textAlign': 'center'}),

        dbc.Nav(
            [dbc.NavLink(item["label"], href=item["href"], active="exact") for item in MENU_ITEMS],
            vertical=True,
            pills=True,
        ),
    ],
    className="bg-primary text-white",
    style={
        'height': '100vh',
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'padding': '20px',
        'margin': '0px',
        'width': '220px'  # Aumentei ligeiramente a largura
    })
    return sidebar

def prepare_and_filter_data(df, selected_year=None, selected_month=None, start_date=None, end_date=None):
    """
    Filtra o DataFrame com base em:
    - Ano (selected_year)
    - Mês (selected_month)
    - Data Inicial e Data Final (start_date, end_date)
    """
    df_filtered = df.copy()

    if selected_year:
        df_filtered = df_filtered[df_filtered['ano'] == selected_year]
    if selected_month:
        df_filtered = df_filtered[df_filtered['mes'] == selected_month]

    df_filtered['data'] = pd.to_datetime(df_filtered['data'])

    if start_date and end_date:
        start_parsed = pd.to_datetime(start_date)
        end_parsed = pd.to_datetime(end_date)
        df_filtered = df_filtered[(df_filtered['data'] >= start_parsed) & (df_filtered['data'] <= end_parsed)]

    return df_filtered

def create_main_content(df, selected_year=None, selected_month=None, start_date=None, end_date=None):
    """
    Cria o conteúdo principal do dashboard.
    Ajustamos tamanhos, margens e paddings para evitar sobreposição
    e deixar o layout mais limpo.
    """
    df_filtered = prepare_and_filter_data(df, selected_year, selected_month, start_date, end_date)

    # Exemplo de cálculo de métricas
    total_quartos = df_filtered['total_quartos'].iloc[0] if not df_filtered.empty else 0
    receita_total = df_filtered['receita_total_dia'].sum()
    receita_total_fmt = format_currency(receita_total, 'BRL', locale='pt_BR')

    ocupacao_media_val = df_filtered['Ocupacao'].mean() if not df_filtered.empty else 0
    ocupacao_media = f"{ocupacao_media_val:.2f}%"

    adr_medio_val = df_filtered['ADR'].mean() if not df_filtered.empty else 0
    adr_medio = format_currency(adr_medio_val, 'BRL', locale='pt_BR')

    gop_medio_val = df_filtered['GOP'].mean() if not df_filtered.empty else 0
    gop_medio = format_currency(gop_medio_val, 'BRL', locale='pt_BR')

    goppar_medio_val = df_filtered['GOPPAR'].mean() if not df_filtered.empty else 0
    goppar_medio = format_currency(goppar_medio_val, 'BRL', locale='pt_BR')

    # Tabela e Gráfico de Rosca
    df_tabela_local = prepare_table_data(df_filtered)
    df_rosca_local = prepare_donut_chart_data(df_filtered)

    rosca_graph = dcc.Graph(
        id='grafico-rosca',
        figure=charts.create_pie_chart(df_rosca_local, names='Tipo', values='Quantidade', title='Tipos de Quartos'),
        style={'height': '350px'}  # Aumentar a altura
    )

    tabela_reservas = dash_table.DataTable(
        data=df_tabela_local.to_dict('records'),
        columns=[
            {'name': 'Cliente', 'id': 'nome_cliente'},
            {'name': 'Data', 'id': 'data'},
            {'name': 'Quarto', 'id': 'tipo_de_quarto'},
            {'name': 'Valor Diárias', 'id': 'valor_total_diarias'}
        ],
        style_cell={'textAlign': 'left', 'fontSize': '14px'},
        style_header={'backgroundColor': 'white', 'fontWeight': 'bold'}
    )

    # Metas (Progress Bars) - Exemplo
    metas_progress = progress_list.create_progress_list([
        {
            "label": "Taxa de Ocupação (80%)",
            "value": 50,
            "color": "warning",
            "style": {"fontSize": "16px", "height": "25px"}
        },
        {
            "label": "RevPAR (R$ 200)",
            "value": 70,
            "color": "success",
            "style": {"fontSize": "16px", "height": "25px"}
        },
        {
            "label": "Conversão de Reservas (10%)",
            "value": 25,
            "color": "danger",
            "style": {"fontSize": "16px", "height": "25px"}
        }
    ])

    main_content = html.Div([
        html.H1('Dashboard Hoteleiro', className="text-center mb-4", style={'fontSize': '24px'}),

        # Linha de Filtros
        dbc.Row([
            # Filtro: Ano
            dbc.Col([
                html.Label("Ano:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='ano-dropdown',
                    options=[{'label': ano, 'value': ano} for ano in sorted(df['ano'].unique())],
                    placeholder="Selecione o Ano",
                    style={'fontSize': '14px'}
                ),
                dbc.Button("Limpar", id='btn-limpar-ano', color='secondary', outline=True, size="sm", className="mt-1")
            ], md=3),

            # Filtro: Mês
            dbc.Col([
                html.Label("Mês:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='mes-dropdown',
                    options=[{'label': mes, 'value': mes} for mes in sorted(df['mes'].unique())],
                    placeholder="Selecione o Mês",
                    style={'fontSize': '14px'}
                ),
                dbc.Button("Limpar", id='btn-limpar-mes', color='secondary', outline=True, size="sm", className="mt-1")
            ], md=3),

            # Filtro: Data Inicial
            dbc.Col([
                html.Label("Data Inicial:", style={'fontWeight': 'bold'}),
                dcc.DatePickerSingle(
                    id='start-date',
                    placeholder='Selecione a Data Inicial',
                    display_format='DD/MM/YYYY',
                    persistence=True,
                    persistence_type='local',
                    style={'fontSize': '14px'}
                ),
                dbc.Button("Limpar", id='btn-limpar-start', color='secondary', outline=True, size="sm", className="mt-1")
            ], md=3),

            # Filtro: Data Final
            dbc.Col([
                html.Label("Data Final:", style={'fontWeight': 'bold'}),
                dcc.DatePickerSingle(
                    id='end-date',
                    placeholder='Selecione a Data Final',
                    display_format='DD/MM/YYYY',
                    persistence=True,
                    persistence_type='local',
                    style={'fontSize': '14px'}
                ),
                dbc.Button("Limpar", id='btn-limpar-end', color='secondary', outline=True, size="sm", className="mt-1")
            ], md=3),
        ], className="mb-3"),

        # Texto de Filtros Selecionados
        dbc.Row([
            dbc.Col(html.P(f"Ano: {selected_year if selected_year else 'Todos'}", style={'fontSize': '14px'}), md=3),
            dbc.Col(html.P(f"Mês: {selected_month if selected_month else 'Todos'}", style={'fontSize': '14px'}), md=3),
            dbc.Col(html.P(f"Data Inicial: {format_date_br(start_date)}", style={'fontSize': '14px'}), md=3),
            dbc.Col(html.P(f"Data Final: {format_date_br(end_date)}", style={'fontSize': '14px'}), md=3)
        ], className="mb-3"),

        # Cards de Resumo (2 Linhas para 6 Cards)
        # Linha 1: "Total de Quartos", "Receita Total", "Ocupação Média"
        dbc.Row([
            dbc.Col(card.create_card("Total de Quartos", total_quartos, color="info", icon="fas fa-home"), md=4),
            dbc.Col(card.create_card("Receita Total", receita_total_fmt, color="success", icon="fas fa-dollar-sign"), md=4),
            dbc.Col(card.create_card("Ocupação Média", ocupacao_media, color="warning", icon="fas fa-chart-bar"), md=4),
        ], className="mb-2"),

        # Linha 2: "ADR Médio", "GOP Médio", "GOPPAR Médio"
        dbc.Row([
            dbc.Col(card.create_card("ADR Médio", adr_medio, color="danger", icon="fas fa-bed"), md=4),
            dbc.Col(card.create_card("GOP Médio", gop_medio, color="primary", icon="fas fa-chart-line"), md=4),
            dbc.Col(card.create_card("GOPPAR Médio", goppar_medio, color="secondary", icon="fas fa-chart-pie"), md=4),
        ], className="mb-3"),

        # Gráfico de Linhas (Receita total)
        dcc.Graph(
            id='grafico-principal',
            figure=charts.create_line_chart(df_filtered, x='data', y='receita_total_dia', title='Receita Total ao Longo do Tempo'),
            style={'height': '300px'}
        ),

        # Gráfico de Rosca e Tabela + Metas
        dbc.Row([
            dbc.Col(
                rosca_graph,
                xs=12, sm=12, md=6, lg=6,
                style={'padding': '5px'}
            ),
            dbc.Col([
                html.H3("Reservas Recentes", className="mb-3", style={'fontSize': '18px'}),
                tabela_reservas,
                html.Br(),
                html.H4("Metas", className="mb-2", style={'fontSize': '18px'}),
                metas_progress
            ],
                xs=12, sm=12, md=6, lg=6,
                style={'padding': '5px'}
            )
        ], className="mb-3"),
    ], style={'marginLeft': '20px', 'marginRight': '20px', 'marginTop': '10px'})

    return main_content

app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP, 
                          "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css"],
    suppress_callback_exceptions=True
)

def create_sidebar():
    """
    Menu lateral fixo (sidebar) com as opções de MENU_ITEMS.
    Ajustamos a largura (width=220px) para evitar sobreposição.
    """
    sidebar = html.Div([
        html.Div([
            html.Img(src=app.get_asset_url('logo.webp'), style={'width': '80%', 'margin': '10px auto', 'display': 'block'}),
            html.Hr(style={'borderColor': '#fff'})
        ], style={'textAlign': 'center'}),
        dbc.Nav(
            [dbc.NavLink(item["label"], href=item["href"], active="exact") for item in MENU_ITEMS],
            vertical=True,
            pills=True
        ),
    ], className="bg-primary text-white",
    style={
        'height': '100vh',
        'position': 'fixed',
        'top': 0,
        'left': 0,
        'padding': '20px',
        'margin': '0px',
        'width': '220px'
    })
    return sidebar

app.layout = dbc.Container([
    dbc.Row([
        # Menu lateral (2 colunas)
        dbc.Col(
            create_sidebar(),
            width=2,
            style={'padding': '0px', 'margin': '0px'}
        ),
        # Conteúdo principal (10 colunas)
        dbc.Col(
            id='main-content',
            width=10,
            children=create_main_content(df),
            style={'padding': '0px', 'margin-left': '220px'}  # Ajuste p/ não sobrepor o menu fixo
        )
    ], style={'margin': '0px'}),
], fluid=True, style={'margin': '0px', 'padding': '0px'})

# CALLBACKS

@app.callback(
    Output('main-content', 'children'),
    [Input('ano-dropdown', 'value'),
     Input('mes-dropdown', 'value'),
     Input('start-date', 'date'),
     Input('end-date', 'date')]
)
def update_main_content(selected_year, selected_month, start_date, end_date):
    """Atualiza o conteúdo principal do dashboard ao mudar qualquer filtro."""
    return create_main_content(df, selected_year, selected_month, start_date, end_date)

@app.callback(
    Output('ano-dropdown', 'value'),
    Input('btn-limpar-ano', 'n_clicks')
)
def limpar_ano(n_clicks):
    if n_clicks:
        return None
    return dash.no_update

@app.callback(
    Output('mes-dropdown', 'value'),
    Input('btn-limpar-mes', 'n_clicks')
)
def limpar_mes(n_clicks):
    if n_clicks:
        return None
    return dash.no_update

@app.callback(
    Output('start-date', 'date'),
    Input('btn-limpar-start', 'n_clicks')
)
def limpar_data_inicial(n_clicks):
    if n_clicks:
        return None
    return dash.no_update

@app.callback(
    Output('end-date', 'date'),
    Input('btn-limpar-end', 'n_clicks')
)
def limpar_data_final(n_clicks):
    if n_clicks:
        return None
    return dash.no_update

if __name__ == "__main__":
    app.run_server(debug=True)
