import pytest

from app.credito.credito import classificar_credito

@pytest.mark.parametrize(
    "renda_mensal, score_credito, restrito, retorno_esperado",
    [
        (0, 10, True, "renda invalida"),
        (-1, -3, True, "renda invalida"),
        (5, -5, False, "score invalido"),
        (3, 1500, False, "score invalido"),
        (3, 500, True, "reprovado"),
        (3, 200, False, "reprovado"),
        (3, 800, False, "aprovado premium"),
    ]
)
def test_classificar_credito_tabela_decisao(
    renda_mensal, score_credito, restrito, retorno_esperado
):
    assert classificar_credito(renda_mensal, score_credito, restrito) == retorno_esperado

@pytest.mark.parametrize(
    "renda_mensal, score_credito, restrito, retorno_esperado",
    [
        (0, 500, False, "renda invalida"),
        (1000, -1, False, "score invalido"),
        (1000, 399, False, "reprovado"),
        (1000, 700, False, "aprovado premium"),
        (1000, 1001, False, "score invalido"),
    ]
)

def test_classificar_credito_limites_criticos(
    renda_mensal, score_credito, restrito, retorno_esperado
):
    assert classificar_credito(renda_mensal, score_credito, restrito) == retorno_esperado