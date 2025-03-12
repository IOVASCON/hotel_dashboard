"""
utils/listar_colunas.py

Script que lê um arquivo CSV (hotel_luxo_jan2000_dez2024.csv) na pasta 'data/'
e lista as colunas encontradas. Pode ser executado diretamente via:
  python utils/listar_colunas.py
estando dentro da pasta 'hotel_dashboard'.
"""

import sys
import os
import pandas as pd

# 1) Ajuste o sys.path para garantir que 'data/' seja localizado
#    Subimos um nível a partir de 'utils/' para chegar em 'hotel_dashboard/',
#    onde está a pasta 'data/'.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def listar_colunas_csv():
    """
    Tenta ler o arquivo CSV em 'data/hotel_luxo_jan2000_dez2024.csv'
    e imprime o nome das colunas encontradas.
    Se ocorrer erro (arquivo não encontrado, etc.), informa o problema.
    """
    # Caminho relativo ao diretório 'hotel_dashboard/'
    csv_path = os.path.join("data", "hotel_luxo_jan2000_dez2024.csv")

    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        print(f"Arquivo não encontrado em: {csv_path}")
        return
    except Exception as e:
        print(f"Erro ao ler o arquivo CSV: {e}")
        return

    print("Nomes das colunas encontradas no CSV:")
    for col in df.columns:
        print(f" - {col}")

if __name__ == "__main__":
    listar_colunas_csv()
