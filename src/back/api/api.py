import requests
import pandas as pd

base_url = "http://ipeadata.gov.br/api/odata4/"
endpoint = "Metadados"

response = requests.get(base_url)

if response.status_code == 200:
    data = response.json()
    registros = data.get("value", [])
    df = pd.DataFrame(registros)
    print(df.head())
else:
    print(f"Erro na requisição: {response.status_code} - {response.text}")
