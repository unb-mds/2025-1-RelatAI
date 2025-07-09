from .dados import carregar_dados
import pandas as pd

def alerta_variacao_diaria(df, nome_serie, percentual_limite=5.0):
    """
    Detecta variações diárias (%) maiores que o limite definido.
    Retorna lista de alertas (datas e mensagens).
    """
    df = df.copy()
    # garante que valor está float
    df['valor'] = df['valor'].astype(str).str.replace(",", ".").astype(float)
    df = df.sort_values('data')
    # calcula variação percentual diária (diferença entre dias consecutivos)
    df['variacao_pct'] = df['valor'].pct_change() * 100

    # detecta variações maiores que limite absoluto
    alertas = []
    for idx, row in df.iterrows():
        if abs(row['variacao_pct']) > percentual_limite:
            alerta_msg = (
                f"Alerta {nome_serie}: variação diária fora do comum em {row['data']} - "
                f"variação de {row['variacao_pct']:.2f}%"
            )
            alertas.append(alerta_msg)
    return alertas

def alerta_valores_extremos(df, nome_serie, desvio_limite=2):
    """
    Detecta valores que estão muito acima ou abaixo da média, usando desvio padrão.
    Retorna lista de alertas.
    """
    df = df.copy()
    df['valor'] = df['valor'].astype(str).str.replace(",", ".").astype(float)
    media = df['valor'].mean()
    desvio = df['valor'].std()

    alertas = []
    for idx, row in df.iterrows():
        if row['valor'] > media + desvio_limite * desvio:
            alertas.append(
                f"Alerta {nome_serie}: valor muito alto em {row['data']} - {row['valor']:.2f}"
            )
        elif row['valor'] < media - desvio_limite * desvio:
            alertas.append(
                f"Alerta {nome_serie}: valor muito baixo em {row['data']} - {row['valor']:.2f}"
            )
    return alertas

def gerar_alertas(dados):
    """
    Recebe dict com DataFrames (selic, cambio, ipca) e retorna todos os alertas.
    """
    alertas = []
    alertas += alerta_variacao_diaria(dados['selic'], "Selic", percentual_limite=1.0)  # mais sensível para Selic
    alertas += alerta_variacao_diaria(dados['cambio'], "Câmbio", percentual_limite=3.0)
    alertas += alerta_variacao_diaria(dados['ipca'], "IPCA", percentual_limite=0.5)

    alertas += alerta_valores_extremos(dados['selic'], "Selic", desvio_limite=2)
    alertas += alerta_valores_extremos(dados['cambio'], "Câmbio", desvio_limite=2)
    alertas += alerta_valores_extremos(dados['ipca'], "IPCA", desvio_limite=2)

    return alertas