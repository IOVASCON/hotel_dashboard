import pandas as pd

def load_and_process_data(file_path):
    """
    Carrega os dados do arquivo CSV e retorna um DataFrame.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except FileNotFoundError:
        print(f"Erro: Arquivo '{file_path}' não encontrado.")
        return None
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        return None
