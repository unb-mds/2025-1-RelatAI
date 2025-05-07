import csv
from django.http import HttpResponse

def exibir_ipca(request):
    caminho_csv = 'data/ipca.csv'
    with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        linhas = ['\t'.join(row) for row in reader]
        texto = '\n'.join(linhas)

    return HttpResponse(texto, content_type='text/plain')

def exibir_igpm(request):
    caminho_csv = 'data/igp.csv'
    with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        linhas = ['\t'.join(row) for row in reader]
        texto = '\n'.join(linhas)

    return HttpResponse(texto, content_type='text/plain')

def exibir_inpc(request):
    caminho_csv = 'data/inpc.csv'
    with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        linhas = ['\t'.join(row) for row in reader]
        texto = '\n'.join(linhas)

    return HttpResponse(texto, content_type='text/plain')

def exibir_cambio(request):
    caminho_csv = 'data/cambio.csv'
    with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        linhas = ['\t'.join(row) for row in reader]
        texto = '\n'.join(linhas)

    return HttpResponse(texto, content_type='text/plain')

def exibir_taxa_de_juros(request):
    caminho_csv = 'data/taxa_de_juros.csv'
    with open(caminho_csv, newline='', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        linhas = ['\t'.join(row) for row in reader]
        texto = '\n'.join(linhas)

    return HttpResponse(texto, content_type='text/plain')