import pandas as pd
from datetime import datetime

# Função para carregar os dados
def load_data(file_path):
    """
    Carrega o DataFrame a partir de um arquivo CSV.
    """
    try:
        df = pd.read_csv(file_path)
        # Converte a coluna 'data' para datetime, assumindo o formato ISO8601 (AAAA-MM-DD)
        df['data'] = pd.to_datetime(df['data'], format='ISO8601')
        return df
    except Exception as e:
        print(f"Erro ao carregar os dados: {e}")
        return None

# Função para filtrar os dados por período
def filter_data_by_date(df, start_date, end_date):
    """
    Filtra o DataFrame pelo período entre start_date e end_date.
    """
    try:
        # Converte as datas de entrada para o formato datetime
        start_date = pd.to_datetime(start_date, format='%d/%m/%Y')
        end_date = pd.to_datetime(end_date, format='%d/%m/%Y')
        # Filtra o DataFrame
        filtered_df = df[(df['data'] >= start_date) & (df['data'] <= end_date)]
        return filtered_df
    except Exception as e:
        print(f"Erro ao filtrar os dados: {e}")
        return None

# Função para calcular as métricas
def calculate_metrics(df):
    """
    Calcula as métricas de Revenue Management.
    """
    try:
        # Total de quartos é fixo (100) e está na sétima coluna
        total_quartos = df['total_quartos'].iloc[0]  # Pega o valor da primeira linha

        # Receita total é a soma da receita total diária
        receita_total = df['receita_total_dia'].sum()

        # Ocupação média é a média de quartos ocupados em relação ao total de quartos
        ocupacao_media = (df['quartos_ocupados_dia'].sum() / (total_quartos * len(df))) * 100

        # ADR Médio é calculado usando a função do dashboard
        adr_medio = calcular_adr(df['receita_quartos_dia'].sum(), df['quartos_ocupados_dia'].sum())

        # GOP Médio é a média do lucro operacional bruto diário
        gop_medio = df['lucro_operacional_bruto_dia'].mean()

        # GOPPAR Médio é a média do GOPPAR diário
        goppar_medio = df['goppar_dia'].mean()

        return {
            'Total Quartos': total_quartos,
            'Receita Total': receita_total,
            'Ocupação Média': ocupacao_media,
            'ADR Médio': adr_medio,
            'GOP Médio': gop_medio,
            'GOPPAR Médio': goppar_medio
        }
    except Exception as e:
        print(f"Erro ao calcular as métricas: {e}")
        return None

# Função para calcular o ADR (idêntica ao dashboard)
def calcular_adr(receita_quartos_dia, quartos_ocupados_dia):
    """
    Calcula a diária média (ADR).
    """
    try:
        return receita_quartos_dia / quartos_ocupados_dia
    except ZeroDivisionError:
        return 0  # Retorna 0 se quartos_ocupados for zero

# Função principal
def main():
    # Caminho para o arquivo CSV
    file_path = 'data/hotel_luxo_jan2000_dez2024.csv'

    # Carregar os dados
    df = load_data(file_path)
    if df is None:
        return

    # Solicitar as datas inicial e final
    start_date = input("Digite a data inicial (DD/MM/AAAA): ")
    end_date = input("Digite a data final (DD/MM/AAAA): ")

    # Filtrar os dados pelo período
    filtered_df = filter_data_by_date(df, start_date, end_date)
    if filtered_df is None:
        return

    # Calcular as métricas
    metrics = calculate_metrics(filtered_df)
    if metrics is None:
        return

    # Exibir os resultados
    print("\nMétricas no período de {} a {}:".format(start_date, end_date))
    for key, value in metrics.items():
        if key == 'ADR Médio':
            print(f"{key}: R$ {value:.2f}")  # Formata o ADR Médio como moeda
        else:
            print(f"{key}: {value:.2f}" if isinstance(value, float) else f"{key}: {value}")

if __name__ == "__main__":
    main()