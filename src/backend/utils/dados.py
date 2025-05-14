# URLs das APIs do Banco Central
URL_SELIC = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.7326/dados?formato=csv&dataInicial=12/05/2015&dataFinal=12/05/2025"
URL_CAMBIO = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.1/dados?formato=csv&dataInicial=12/05/2015&dataFinal=12/05/2025"
URL_IPCA = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.433/dados?formato=csv"  # IPCA é mensal, não precisa limitar


# Baixar dados diretamente (sem tratamento)
response_selic = requests.get(URL_SELIC)
response_cambio = requests.get(URL_CAMBIO)
response_ipca = requests.get(URL_IPCA)

# Converter respostas em DataFrame bruto
df_selic = pd.read_csv(StringIO(response_selic.text), sep=";", decimal=",") #Transform de tipo texto em String, declara que ; é separação, e declara que ontem tem número com , signific que é decimal e transforma para .
df_cambio = pd.read_csv(StringIO(response_cambio.text), sep=";", decimal=",")
df_ipca = pd.read_csv(StringIO(response_ipca.text), sep=";", decimal=",")
pd.set_option('display.max_columns', None) #mostrar o maximo de colunas existentes