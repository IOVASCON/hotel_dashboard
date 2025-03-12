import plotly.express as px

def create_line_chart(df, x, y, title):
    """
    Cria um gráfico de linhas (line chart) com os dados fornecidos, aplicando estilo e formatação.
    
    :param df: DataFrame com os dados
    :param x: Nome da coluna para o eixo X
    :param y: Nome da coluna para o eixo Y
    :param title: Título do gráfico
    :return: Objeto Figure do Plotly com o gráfico de linhas
    """
    try:
        # Verifica se o DataFrame está vazio
        if df.empty:
            print("DataFrame vazio em create_line_chart(). Retornando gráfico em branco.")
            return px.line()

        # Cria o gráfico de linhas
        fig = px.line(df, x=x, y=y, title=title)
        
        # Ajusta o layout do gráfico
        fig.update_layout(
            title_x=0.5,
            plot_bgcolor='rgba(0,0,0,0)',   # fundo transparente do plot
            paper_bgcolor='rgba(0,0,0,0)',  # fundo transparente do "papel"
            font=dict(size=14),             # tamanho da fonte geral
            legend=dict(font=dict(size=14)),# tamanho da fonte da legenda
            title=dict(font=dict(size=16))  # tamanho da fonte do título
        )
        
        # Ajusta o estilo das linhas (espessura)
        fig.update_traces(line=dict(width=2))

        return fig
    except Exception as e:
        print(f"Erro ao criar o gráfico de linhas: {e}")
        return None

def create_pie_chart(df, names, values, title):
    """
    Cria um gráfico de pizza/doce (pie chart) com os dados fornecidos, aplicando estilo e formatação.
    
    :param df: DataFrame com os dados
    :param names: Nome da coluna que define as fatias (labels)
    :param values: Nome da coluna que define os valores (quantidade, soma, etc.)
    :param title: Título do gráfico
    :return: Objeto Figure do Plotly com o gráfico de pizza (ou rosca, se houver 'hole')
    """
    try:
        # Verifica se o DataFrame está vazio
        if df.empty:
            print("DataFrame vazio em create_pie_chart(). Retornando gráfico em branco.")
            return px.pie()

        # Cria o gráfico de pizza/rosca
        fig = px.pie(df, names=names, values=values, hole=0.3, title=title)
        
        # Ajuste do layout: legenda, fundo, fonte etc.
        fig.update_layout(
            title_x=0.5,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=14),             # tamanho da fonte geral
            title=dict(font=dict(size=16)),
            legend=dict(
                x=0.7,                     # aproxima a legenda do gráfico (ajuste x conforme necessário)
                y=0.5,
                font=dict(size=16)         # fonte maior para as legendas (Suite, Duplo, Standart)
            )
        )
        
        # Ajusta o tamanho da fonte do texto interno (percentuais, labels)
        fig.update_traces(textfont_size=16)

        return fig
    except Exception as e:
        print(f"Erro ao criar o gráfico de pizza: {e}")
        return None
