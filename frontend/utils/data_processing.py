import pandas as pd
import numpy as np

def process_api_data(df):
    try:
        if df is None or df.empty:
            print("Aviso: DataFrame vazio recebido")
            return None

        print(f"Tipo de dados recebidos: {type(df)}")
        print(f"Colunas no DataFrame: {df.columns.tolist()}")
        print(f"Primeiras 2 linhas:\n{df.head(2)}")

        # Verificar se as colunas necessárias existem
        if 'data' not in df.columns or 'valor' not in df.columns:
            print("Aviso: Dados recebidos não contêm as colunas esperadas ('data' e 'valor')")
            return None

        # Garantir que a coluna 'data' está em datetime
        if not pd.api.types.is_datetime64_any_dtype(df['data']):
            try:
                df['data'] = pd.to_datetime(df['data'], dayfirst=True)
                print("Conversão de data bem-sucedida")
            except Exception as date_err:
                print(f"Erro na conversão de datas: {date_err}")
                return None

        # Garantir que a coluna 'valor' está em formato numérico
        try:
            if df['valor'].dtype == 'object':
                df['valor'] = df['valor'].str.replace(',', '.', regex=False)
            df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
            print(f"NaN após conversão numérica: {df['valor'].isna().sum()}")
        except Exception as val_err:
            print(f"Erro na conversão de valores: {val_err}")
            return None

        # Remover NaN
        before_count = len(df)
        df = df.dropna(subset=['valor', 'data'])
        after_count = len(df)
        print(f"Registros removidos por NaN: {before_count - after_count}")

        # Verificar se ainda há dados após limpeza
        if df.empty or len(df) < 2:
            print("Aviso: Dados insuficientes após limpeza")
            return None

        # Ordenar por data
        df = df.sort_values('data')

        print(f"Dados processados com sucesso: {len(df)} registros válidos")
        return df

    except Exception as e:
        import traceback
        print(f"Erro ao processar dados: {str(e)}\n{traceback.format_exc()}")
        return None

def calculate_statistics(df):
    if df is None or df.empty:
        return None

    stats = {
        'média': df['valor'].mean(),
        'mediana': df['valor'].median(),
        'min': df['valor'].min(),
        'max': df['valor'].max(),
        'desvio_padrão': df['valor'].std(),
        'variação_percentual': ((df['valor'].iloc[-1] / df['valor'].iloc[0]) - 1) * 100 if len(df) > 1 else 0
    }

    return stats

def prepare_data_for_ml(df, window_size=5):
    if df is None or df.empty or len(df) <= window_size:
        return None, None

    values = df['valor'].values

    X, y = [], []
    for i in range(len(values) - window_size):
        X.append(values[i:i + window_size])
        y.append(values[i + window_size])

    return np.array(X), np.array(y)
