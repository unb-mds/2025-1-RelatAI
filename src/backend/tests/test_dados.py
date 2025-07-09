import pytest
import utils.dados as dados
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_carregar_dados_sucesso():
    resultado = dados.carregar_dados()
    
    assert resultado is not None
    assert "selic" in resultado
    assert "ipca" in resultado
    assert not resultado["selic"].empty
    assert not resultado["ipca"].empty
    assert "data" in resultado["selic"].columns
    assert "valor" in resultado["selic"].columns

def test_atualizar_dados_retorna_atualizado():
    dados_iniciais = dados.carregar_dados()
    atualizados = dados.atualizar_dados(
        dados_iniciais["selic"],
        dados_iniciais["cambio"],
        dados_iniciais["ipca"],
        dados_iniciais["pib"],
        dados_iniciais["divida"],
        dados_iniciais["desemprego"]
    )
    
    for key in dados_iniciais:
        assert not dados_iniciais[key].empty