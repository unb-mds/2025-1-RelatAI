import pytest
import pandas as pd
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.alertas import gerar_alertas


sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


@pytest.fixture
def dados_de_teste():
    datas = pd.date_range("2023-01-01", periods=10, freq="D").strftime("%d/%m/%Y")
    
    selic = pd.DataFrame({
        "data": datas,
        "valor": [13.75, 13.75, 13.75, 13.75, 14.00, 13.75, 13.75, 13.75, 13.75, 13.75]
    })
    
    cambio = pd.DataFrame({
        "data": datas,
        "valor": [5.00, 5.10, 5.50, 4.80, 5.20, 6.00, 4.00, 5.00, 5.10, 5.20]  # grandes variações
    })
    
    ipca = pd.DataFrame({
        "data": datas,
        "valor": [0.25, 0.30, 0.20, 0.90, 0.10, 0.30, 0.60, 0.10, 0.50, 0.20]  # inclui extremos
    })
    
    return {
        "selic": selic,
        "cambio": cambio,
        "ipca": ipca
    }

def test_gerar_alertas_retorna_alertas(dados_de_teste):
    alertas = gerar_alertas(dados_de_teste)
    
    # Verifica se retornou uma lista
    assert isinstance(alertas, list)
    
    # Espera-se que existam alertas com os dados simulados
    assert len(alertas) > 0

    # Checa se os alertas têm strings com as palavras-chave
    assert any("Selic" in alerta for alerta in alertas)
    assert any("Câmbio" in alerta for alerta in alertas)
    assert any("IPCA" in alerta for alerta in alertas)

def test_alerta_formato_mensagem(dados_de_teste):
    alertas = gerar_alertas(dados_de_teste)
    
    for alerta in alertas:
        assert "Alerta" in alerta
        assert "-" in alerta  # Deve conter data e valor formatado
