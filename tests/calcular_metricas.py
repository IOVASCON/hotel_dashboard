"""
tests/calcular_metricas.py

Script Python que carrega os dados do arquivo CSV, calcula as métricas de Revenue Management
e imprime os resultados formatados. Ajustado para rodar diretamente com `python tests/calcular_metricas.py`
a partir da pasta `hotel_dashboard`.
"""

import sys, os
import pandas as pd
from babel.numbers import format_currency

# 1) Insira o diretório 'hotel_dashboard' no sys.path, para que 'utils' e 'data_processing'
#    fiquem acessíveis como módulos irmãos de 'tests'.
#    Aqui, __file__ é "tests/calcular_metricas.py". Pegamos o dirname duas vezes:
#      - uma vez para chegar em "tests"
#      - outra vez para chegar em "hotel_dashboard"
#    Mas como já estamos DENTRO de "hotel_dashboard", basta subir um nível para sair de "tests".
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# 2) Agora podemos importar 'utils' e 'data_processing' normalmente
from utils import helpers
from data_processing import process_data

# Caminho do arquivo CSV
DATA_FILE = "data/hotel_luxo_jan2000_dez2024.csv"

def load_data():
    """Carrega os dados do arquivo CSV, usando process_data."""
    df = process_data.load_and_process_data(DATA_FILE)
    if df is None:
        print("Erro ao carregar os dados. O aplicativo não pode continuar.")
        sys.exit(1)
    return df

def calculate_metrics(df):
    """Calcula as métricas do hotel."""
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
        sys.exit(1)

# 1) Carregar os dados
df = load_data()

# 2) Calcular as métricas
df = calculate_metrics(df)

# 3) Extrair e resumir as principais métricas
total_quartos = df['total_quartos'].iloc[0]
receita_total = df['receita_total_dia'].sum()
ocupacao_media = df['Ocupacao'].mean()
adr_medio = df['ADR'].mean()
gop_medio = df['GOP'].mean()
goppar_medio = df['GOPPAR'].mean()

# 4) Formatar os resultados
receita_total_formatada = format_currency(receita_total, 'BRL', locale='pt_BR')
adr_medio_formatado = format_currency(adr_medio, 'BRL', locale='pt_BR')
gop_medio_formatado = format_currency(gop_medio, 'BRL', locale='pt_BR')
goppar_medio_formatado = format_currency(goppar_medio, 'BRL', locale='pt_BR')
ocupacao_media_formatada = f"{ocupacao_media:.2f}%"

# 5) Imprimir os resultados
print("Métricas do Hotel:")
print(f"  Total de Quartos: {total_quartos}")
print(f"  Receita Total: {receita_total_formatada}")
print(f"  Ocupação Média: {ocupacao_media_formatada}")
print(f"  ADR Médio: {adr_medio_formatado}")
print(f"  GOP Médio: {gop_medio_formatado}")
print(f"  GOPPAR Médio: {goppar_medio_formatado}")
