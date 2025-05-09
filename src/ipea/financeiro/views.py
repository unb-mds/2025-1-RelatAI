import requests
from django.http import HttpResponse

def ver_tabelas(titulo, url):

    try:
        response = requests.get(url)
        response.raise_for_status()
        dados_json = response.json()

        html = """
        <html>
            <head>
                <title> Taxas </title>
                <style>
                    table {
                        border-collapse: collapse;
                        width: 50%;
                        margin: 20px auto;
                        font-family: Arial, sans-serif;
                    }
                    th, td {
                        border: 1px solid #ccc;
                        padding: 8px;
                        text-align: center;
                    }
                    th {
                        background-color: #f2f2f2;
                    }
                </style>
            </head>
            <body>
                <h2 style="text-align: center;">Valores da série histórica</h2>
                <table>
                    <tr>
                        <th>Data</th>
                        <th>Valor</th>
                    </tr>
        """

        for item in dados_json:
            html += f"<tr><td>{item['data']}</td><td>{item['valor']}</td></tr>"

        html += """
                </table>
            </body>
        </html>
        """

        return HttpResponse(html)

    except requests.RequestException as e:
        return HttpResponse(f"Erro na requisição: {e}", status=500)

def selic(request):
    url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json&dataInicial=01/05/2025'
    return ver_tabelas('Taxa SELIC', url)

def ipca(request):
    url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.10843/dados?formato=json&dataInicial=01/02/2025'
    return ver_tabelas('Taxa IPCA', url)

def cambio(request):
    url = 'https://api.bcb.gov.br/dados/serie/bcdata.sgs.10813/dados?formato=json&dataInicial=01/05/2025'
    return ver_tabelas('Taxa Cambio', url)