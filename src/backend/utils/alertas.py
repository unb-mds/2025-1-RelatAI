from .dados import carregar_dados

# Gera alertas para anos com média de gastos superior a R$10 milhões
def gerar_alertas():
    df = carregar_dados()
    media_gastos = df.groupby("ano")["valor"].mean()
    alertas = []
    for ano, valor in media_gastos.items():
        if valor > 10000000:
            alertas.append(f"🚨 Alerta: Média de gastos em {ano} ultrapassou R$10 milhões")
    return alertas
